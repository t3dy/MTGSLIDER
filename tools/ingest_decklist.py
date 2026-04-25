"""Ingest a decklist .md file into MTGSLIDER's `decklists` and `decklist_cards` tables.

Usage:
    python tools/ingest_decklist.py decklists/HOGAAK_BRIDGEVINE_MC_BARCELONA_2019.md

The .md file must have YAML frontmatter (slug, name, archetype, format, event_*, pilot,
source_url) and a "Cleaned mainboard" / "Sideboard" section formatted as markdown tables
with columns `Qty | Card | Role`. The parser is regex-based and tolerant of extra columns.

No LLM calls. Card names are fuzzy-matched via Scryfall.
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

from mtgslider import scryfall, themes  # noqa: E402
from mtgslider.db import connect  # noqa: E402

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
TABLE_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|")  # | qty | card | ...
SECTION_RE = re.compile(r"^##\s+(Cleaned mainboard|Sideboard)\b", re.IGNORECASE)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FM_RE.match(text)
    if not m:
        raise ValueError("file has no YAML frontmatter")
    fm: dict = {}
    for raw in m.group(1).splitlines():
        line = raw.rstrip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    return fm, m.group(2)


def parse_decklist_sections(body: str) -> dict[str, list[tuple[int, str]]]:
    """Returns {'mainboard': [(qty, name), ...], 'sideboard': [...]}."""
    out: dict[str, list[tuple[int, str]]] = {"mainboard": [], "sideboard": []}
    current = None
    for line in body.splitlines():
        sec = SECTION_RE.match(line)
        if sec:
            current = "sideboard" if "sideboard" in sec.group(1).lower() else "mainboard"
            continue
        if current is None:
            continue
        m = TABLE_ROW_RE.match(line)
        if not m:
            continue
        qty = int(m.group(1))
        name = m.group(2).strip()
        if name.lower() in ("card",):
            continue  # header row
        out[current].append((qty, name))
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("decklist_md", help="path to a decklist .md file")
    args = p.parse_args()

    md_path = Path(args.decklist_md).resolve()
    text = md_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    sections = parse_decklist_sections(body)

    if not sections["mainboard"]:
        print(f"ERROR: no mainboard rows parsed from {md_path}", file=sys.stderr)
        return 2

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with connect() as conn:
        existing = conn.execute("SELECT id FROM decklists WHERE slug = ?", (fm["slug"],)).fetchone()
        if existing:
            decklist_id = existing["id"]
            conn.execute(
                """UPDATE decklists SET
                    name=?, archetype=?, format=?, event_name=?, event_date=?,
                    placement=?, pilot=?, source_url=?, notes_markdown=?, updated_at=?
                   WHERE id=?""",
                (
                    fm.get("name", fm["slug"]),
                    fm.get("archetype"),
                    fm.get("format", "Unknown"),
                    fm.get("event_name"),
                    fm.get("event_date"),
                    fm.get("placement"),
                    fm.get("pilot"),
                    fm.get("source_url"),
                    body.strip(),
                    now,
                    decklist_id,
                ),
            )
            conn.execute("DELETE FROM decklist_cards WHERE decklist_id = ?", (decklist_id,))
        else:
            cur = conn.execute(
                """INSERT INTO decklists
                    (slug, name, archetype, format, event_name, event_date,
                     placement, pilot, source_url, notes_markdown, created_at, updated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    fm["slug"],
                    fm.get("name", fm["slug"]),
                    fm.get("archetype"),
                    fm.get("format", "Unknown"),
                    fm.get("event_name"),
                    fm.get("event_date"),
                    fm.get("placement"),
                    fm.get("pilot"),
                    fm.get("source_url"),
                    body.strip(),
                    now,
                    now,
                ),
            )
            decklist_id = cur.lastrowid

        n_cards = n_unresolved = 0
        for location, rows in sections.items():
            for qty, name in rows:
                card = scryfall.named(name, fuzzy=True)
                if card is None:
                    print(f"  unresolved: {name}", file=sys.stderr)
                    n_unresolved += 1
                    continue
                themes.upsert_card(card, conn=conn)
                conn.execute(
                    """INSERT OR REPLACE INTO decklist_cards
                        (decklist_id, scryfall_id, quantity, location)
                        VALUES (?,?,?,?)""",
                    (decklist_id, card.id, qty, location),
                )
                n_cards += 1
        conn.commit()

    print(f"OK: ingested {fm['slug']!r}  cards={n_cards}  unresolved={n_unresolved}")
    return 0 if n_unresolved == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
