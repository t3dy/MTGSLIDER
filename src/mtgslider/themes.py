"""Theme service: create themes, link Scryfall cards, mark review status."""
from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

from . import scryfall
from .db import connect
from .images import DEFAULT_VARIANT, fetch_card_images
from .paths import theme_dir
from .scryfall import Card

_SLUG_BAD = re.compile(r"[^a-z0-9]+")


def slugify(name: str) -> str:
    s = _SLUG_BAD.sub("-", name.lower()).strip("-")
    return s or "theme"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------- theme CRUD ----------

def create_theme(
    canonical_name: str,
    *,
    short_description: Optional[str] = None,
    aliases: Iterable[str] = (),
    conn: Optional[sqlite3.Connection] = None,
) -> dict:
    own_conn = conn is None
    conn = conn or connect()
    try:
        slug = slugify(canonical_name)
        now = _now()
        cur = conn.execute(
            "INSERT INTO themes (slug, canonical_name, short_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (slug, canonical_name, short_description, now, now),
        )
        theme_id = cur.lastrowid
        for alias in aliases:
            conn.execute(
                "INSERT OR IGNORE INTO theme_aliases (theme_id, alias) VALUES (?, ?)",
                (theme_id, alias),
            )
        conn.commit()
        theme_dir(slug)
        return get_theme(slug, conn=conn)
    finally:
        if own_conn:
            conn.close()


def get_theme(slug: str, *, conn: Optional[sqlite3.Connection] = None) -> dict:
    own_conn = conn is None
    conn = conn or connect()
    try:
        row = conn.execute("SELECT * FROM themes WHERE slug = ?", (slug,)).fetchone()
        if row is None:
            raise KeyError(f"no theme with slug {slug!r}")
        aliases = [
            r["alias"]
            for r in conn.execute(
                "SELECT alias FROM theme_aliases WHERE theme_id = ?", (row["id"],)
            ).fetchall()
        ]
        return {**dict(row), "aliases": aliases}
    finally:
        if own_conn:
            conn.close()


def list_themes(*, conn: Optional[sqlite3.Connection] = None) -> list[dict]:
    own_conn = conn is None
    conn = conn or connect()
    try:
        rows = conn.execute(
            "SELECT slug, canonical_name, research_status, updated_at FROM themes ORDER BY updated_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        if own_conn:
            conn.close()


def set_research_status(slug: str, status: str, *, conn: Optional[sqlite3.Connection] = None) -> None:
    own_conn = conn is None
    conn = conn or connect()
    try:
        conn.execute(
            "UPDATE themes SET research_status = ?, updated_at = ? WHERE slug = ?",
            (status, _now(), slug),
        )
        conn.commit()
    finally:
        if own_conn:
            conn.close()


# ---------- card cache ----------

def upsert_card(card: Card, *, conn: sqlite3.Connection) -> None:
    conn.execute(
        """INSERT INTO cards (
            scryfall_id, oracle_id, name, type_line, mana_cost, oracle_text,
            colors, color_identity, legalities, set_code, set_name, rarity,
            artist, image_uris, scryfall_uri, layout, raw_json, fetched_at
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(scryfall_id) DO UPDATE SET
            name=excluded.name,
            type_line=excluded.type_line,
            mana_cost=excluded.mana_cost,
            oracle_text=excluded.oracle_text,
            colors=excluded.colors,
            color_identity=excluded.color_identity,
            legalities=excluded.legalities,
            image_uris=excluded.image_uris,
            scryfall_uri=excluded.scryfall_uri,
            raw_json=excluded.raw_json,
            fetched_at=excluded.fetched_at""",
        (
            card.id,
            card.oracle_id,
            card.name,
            card.type_line,
            card.mana_cost,
            card.oracle_text,
            json.dumps(card.colors),
            json.dumps(card.color_identity),
            json.dumps(card.legalities),
            card.set_code,
            card.set_name,
            card.rarity,
            card.artist,
            json.dumps(card.image_uris),
            card.scryfall_uri,
            card.layout,
            json.dumps(card.to_dict()),
            _now(),
        ),
    )


def get_cached_card(scryfall_id: str, *, conn: sqlite3.Connection) -> Optional[Card]:
    row = conn.execute("SELECT raw_json FROM cards WHERE scryfall_id = ?", (scryfall_id,)).fetchone()
    if row is None:
        return None
    return _card_from_to_dict(json.loads(row["raw_json"]))


def _card_from_to_dict(d: dict) -> Card:
    faces_data = d.pop("faces", []) or []
    card = Card(**d)
    card.faces = [_card_from_to_dict(f) for f in faces_data]
    return card


# ---------- linking ----------

def add_link(
    *,
    theme_slug: str,
    card: Card,
    link_type: str,
    link_reason: str = "",
    confidence: float = 0.5,
    include_status: str = "uncertain",
    conn: Optional[sqlite3.Connection] = None,
) -> int:
    own_conn = conn is None
    conn = conn or connect()
    try:
        theme = get_theme(theme_slug, conn=conn)
        upsert_card(card, conn=conn)
        now = _now()
        cur = conn.execute(
            """INSERT INTO theme_card_links
                (theme_id, scryfall_id, link_type, link_reason, confidence, include_status, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?)
                ON CONFLICT(theme_id, scryfall_id, link_type) DO UPDATE SET
                    link_reason=excluded.link_reason,
                    confidence=excluded.confidence,
                    updated_at=excluded.updated_at""",
            (theme["id"], card.id, link_type, link_reason, confidence, include_status, now, now),
        )
        conn.commit()
        return cur.lastrowid or 0
    finally:
        if own_conn:
            conn.close()


def find_cards_by_query(
    theme_slug: str,
    query: str,
    *,
    limit: Optional[int] = None,
    confidence: float = 0.5,
    conn: Optional[sqlite3.Connection] = None,
) -> int:
    """Run a Scryfall query and stage results as theme_card_links (uncertain)."""
    own_conn = conn is None
    conn = conn or connect()
    try:
        added = 0
        for card in scryfall.search(query):
            add_link(
                theme_slug=theme_slug,
                card=card,
                link_type="scryfall_query",
                link_reason=f"query: {query}",
                confidence=confidence,
                include_status="uncertain",
                conn=conn,
            )
            added += 1
            if limit is not None and added >= limit:
                break
        return added
    finally:
        if own_conn:
            conn.close()


def add_card_by_name(
    theme_slug: str,
    card_name: str,
    *,
    fuzzy: bool = True,
    include_status: str = "include",
    conn: Optional[sqlite3.Connection] = None,
) -> Optional[Card]:
    card = scryfall.named(card_name, fuzzy=fuzzy)
    if card is None:
        return None
    add_link(
        theme_slug=theme_slug,
        card=card,
        link_type="manual",
        link_reason=f"manual add: {card_name}",
        confidence=1.0,
        include_status=include_status,
        conn=conn,
    )
    return card


def list_links(
    theme_slug: str,
    *,
    include_status: Optional[str] = None,
    conn: Optional[sqlite3.Connection] = None,
) -> list[dict]:
    own_conn = conn is None
    conn = conn or connect()
    try:
        theme = get_theme(theme_slug, conn=conn)
        if include_status:
            rows = conn.execute(
                """SELECT l.*, c.name AS card_name, c.type_line, c.mana_cost
                    FROM theme_card_links l JOIN cards c ON c.scryfall_id = l.scryfall_id
                    WHERE l.theme_id = ? AND l.include_status = ?
                    ORDER BY c.name""",
                (theme["id"], include_status),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT l.*, c.name AS card_name, c.type_line, c.mana_cost
                    FROM theme_card_links l JOIN cards c ON c.scryfall_id = l.scryfall_id
                    WHERE l.theme_id = ?
                    ORDER BY l.include_status, c.name""",
                (theme["id"],),
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        if own_conn:
            conn.close()


def mark_card(
    theme_slug: str,
    card_name: str,
    *,
    include_status: Optional[str] = None,
    review_status: Optional[str] = None,
    note: Optional[str] = None,
    conn: Optional[sqlite3.Connection] = None,
) -> int:
    """Update all links for the named card under this theme."""
    own_conn = conn is None
    conn = conn or connect()
    try:
        theme = get_theme(theme_slug, conn=conn)
        rows = conn.execute(
            """SELECT l.id FROM theme_card_links l JOIN cards c ON c.scryfall_id = l.scryfall_id
                WHERE l.theme_id = ? AND lower(c.name) = lower(?)""",
            (theme["id"], card_name),
        ).fetchall()
        if not rows:
            raise KeyError(f"no card named {card_name!r} linked to theme {theme_slug!r}")
        sets, params = [], []
        if include_status:
            sets.append("include_status = ?")
            params.append(include_status)
        if review_status:
            sets.append("review_status = ?")
            params.append(review_status)
        if note is not None:
            sets.append("note = ?")
            params.append(note)
        if not sets:
            return 0
        sets.append("updated_at = ?")
        params.append(_now())
        ids = [r["id"] for r in rows]
        placeholders = ",".join("?" for _ in ids)
        conn.execute(
            f"UPDATE theme_card_links SET {', '.join(sets)} WHERE id IN ({placeholders})",
            (*params, *ids),
        )
        conn.commit()
        return len(ids)
    finally:
        if own_conn:
            conn.close()


# ---------- images ----------

def fetch_images_for_theme(
    theme_slug: str,
    *,
    variant: str = DEFAULT_VARIANT,
    only_included: bool = True,
    conn: Optional[sqlite3.Connection] = None,
) -> int:
    own_conn = conn is None
    conn = conn or connect()
    try:
        theme = get_theme(theme_slug, conn=conn)
        out_dir = theme_dir(theme["slug"]) / "images"
        statuses = ("include", "exemplar") if only_included else ("include", "exemplar", "uncertain")
        placeholders = ",".join("?" for _ in statuses)
        rows = conn.execute(
            f"""SELECT DISTINCT l.scryfall_id FROM theme_card_links l
                WHERE l.theme_id = ? AND l.include_status IN ({placeholders})""",
            (theme["id"], *statuses),
        ).fetchall()
        count = 0
        for row in rows:
            card = get_cached_card(row["scryfall_id"], conn=conn)
            if card is None:
                continue
            records = fetch_card_images(card, variant, out_dir=out_dir)
            for rec in records:
                conn.execute(
                    """INSERT OR REPLACE INTO theme_card_images
                        (theme_id, scryfall_id, face_index, face_name, variant, source_url, local_path, downloaded_at)
                        VALUES (?,?,?,?,?,?,?,?)""",
                    (
                        theme["id"],
                        rec.scryfall_id,
                        rec.face_index,
                        rec.face_name,
                        rec.variant,
                        rec.source_url,
                        str(rec.local_path),
                        rec.downloaded_at,
                    ),
                )
                count += 1
        conn.commit()
        return count
    finally:
        if own_conn:
            conn.close()


def list_images(
    theme_slug: str,
    *,
    variant: Optional[str] = None,
    conn: Optional[sqlite3.Connection] = None,
) -> list[dict]:
    own_conn = conn is None
    conn = conn or connect()
    try:
        theme = get_theme(theme_slug, conn=conn)
        if variant:
            rows = conn.execute(
                """SELECT i.*, c.name AS card_name FROM theme_card_images i
                    JOIN cards c ON c.scryfall_id = i.scryfall_id
                    WHERE i.theme_id = ? AND i.variant = ?
                    ORDER BY c.name, i.face_index""",
                (theme["id"], variant),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT i.*, c.name AS card_name FROM theme_card_images i
                    JOIN cards c ON c.scryfall_id = i.scryfall_id
                    WHERE i.theme_id = ?
                    ORDER BY c.name, i.face_index""",
                (theme["id"],),
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        if own_conn:
            conn.close()
