"""Ingest historical-trip research cards (markdown with YAML frontmatter) into SQLite.

Usage:
    python tools/ingest_historical_trips.py [--root writing/historical_trips]

Reads every .md file with YAML frontmatter under the root, parses (slug, source_type,
title, summary, confidence, review_status, mtg_card_refs, mtg_theme_refs), and
upserts a row in `historical_trips` plus rows in `trip_card_refs`.

No LLM calls. Pure parsing.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mtgslider import scryfall  # noqa: E402
from mtgslider.db import connect  # noqa: E402

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FM_RE.match(text)
    if not m:
        raise ValueError("file has no YAML frontmatter")
    fm_block, body = m.group(1), m.group(2)
    fm: dict = {}
    for raw_line in fm_block.splitlines():
        line = raw_line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        # Inline list: [a, b, c] or empty []
        if val.startswith("[") and val.endswith("]"):
            inside = val[1:-1].strip()
            fm[key] = [s.strip() for s in inside.split(",") if s.strip()] if inside else []
        else:
            fm[key] = val
    return fm, body


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=str(ROOT / "writing" / "historical_trips"))
    args = p.parse_args()

    root = Path(args.root)
    md_files = sorted(root.rglob("*.md"))
    md_files = [f for f in md_files if f.name not in ("INDEX.md", "README.md")]

    n_ok = n_skipped = 0
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with connect() as conn:
        for md in md_files:
            text = md.read_text(encoding="utf-8")
            try:
                fm, body = parse_frontmatter(text)
            except ValueError:
                print(f"SKIP (no frontmatter): {md.relative_to(ROOT)}")
                n_skipped += 1
                continue
            slug = fm.get("slug")
            if not slug:
                print(f"SKIP (no slug): {md.relative_to(ROOT)}")
                n_skipped += 1
                continue
            existing = conn.execute("SELECT id FROM historical_trips WHERE slug = ?", (slug,)).fetchone()
            if existing:
                conn.execute(
                    """UPDATE historical_trips SET
                        source_type=?, title=?, summary=?, body_markdown=?, source_path=?,
                        confidence=?, review_status=?, updated_at=?
                       WHERE slug=?""",
                    (
                        fm.get("source_type", "etymology"),
                        fm.get("title", slug),
                        fm.get("summary", ""),
                        body.strip(),
                        str(md.relative_to(ROOT)),
                        fm.get("confidence", "medium"),
                        fm.get("review_status", "unreviewed"),
                        now,
                        slug,
                    ),
                )
                trip_id = existing["id"]
            else:
                cur = conn.execute(
                    """INSERT INTO historical_trips
                        (slug, source_type, title, summary, body_markdown, source_path,
                         confidence, review_status, created_at, updated_at)
                        VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (
                        slug,
                        fm.get("source_type", "etymology"),
                        fm.get("title", slug),
                        fm.get("summary", ""),
                        body.strip(),
                        str(md.relative_to(ROOT)),
                        fm.get("confidence", "medium"),
                        fm.get("review_status", "unreviewed"),
                        now,
                        now,
                    ),
                )
                trip_id = cur.lastrowid

            # Refresh refs
            conn.execute("DELETE FROM trip_card_refs WHERE trip_id = ?", (trip_id,))
            for card_name in fm.get("mtg_card_refs", []):
                card = scryfall.named(card_name, fuzzy=True)
                if card is None:
                    continue
                conn.execute(
                    "INSERT OR IGNORE INTO trip_card_refs (trip_id, scryfall_id, theme_slug, relevance, note) VALUES (?,?,?,?,?)",
                    (trip_id, card.id, None, "high", f"named ref: {card_name}"),
                )
            for theme_slug in fm.get("mtg_theme_refs", []):
                conn.execute(
                    "INSERT OR IGNORE INTO trip_card_refs (trip_id, scryfall_id, theme_slug, relevance, note) VALUES (?,?,?,?,?)",
                    (trip_id, None, theme_slug, "medium", "named theme ref"),
                )
            print(f"OK: {slug:25s}  ({fm.get('source_type','?')})")
            n_ok += 1
        conn.commit()

    print(f"\ndone. ok={n_ok} skipped={n_skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
