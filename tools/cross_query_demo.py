"""Cross-query demo: which cards in the Hogaak Bridgevine deck also belong to
themes already in MTGSLIDER's database?

Writes a markdown report to writing/CROSS_QUERY_HOGAAK_DEMO.md.

This is the proof-of-architecture artifact: it joins decklist_cards (Q22 / Deckard D6),
theme_card_links (existing slice 1), and historical_trips (Q22 new) in one query.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mtgslider.db import connect  # noqa: E402

DECK_SLUG = "hogaak-bridgevine-mc-barcelona-2019"
OUT = ROOT / "writing" / "CROSS_QUERY_HOGAAK_DEMO.md"


def main() -> int:
    with connect() as conn:
        deck = conn.execute("SELECT * FROM decklists WHERE slug = ?", (DECK_SLUG,)).fetchone()
        if not deck:
            print(f"ERROR: no decklist with slug {DECK_SLUG!r}; run ingest first", file=sys.stderr)
            return 2

        cards = conn.execute(
            """SELECT dc.quantity, dc.location, c.name, c.scryfall_id
               FROM decklist_cards dc JOIN cards c ON c.scryfall_id = dc.scryfall_id
               WHERE dc.decklist_id = ?
               ORDER BY dc.location, c.name""",
            (deck["id"],),
        ).fetchall()

        # For each unique scryfall_id, find theme links
        theme_hits = conn.execute(
            """SELECT DISTINCT c.name, c.scryfall_id, t.slug AS theme_slug, t.canonical_name AS theme_name,
                       l.include_status
               FROM decklist_cards dc
               JOIN cards c ON c.scryfall_id = dc.scryfall_id
               JOIN theme_card_links l ON l.scryfall_id = dc.scryfall_id
               JOIN themes t ON t.id = l.theme_id
               WHERE dc.decklist_id = ?
               ORDER BY t.canonical_name, c.name""",
            (deck["id"],),
        ).fetchall()

        trip_refs = conn.execute(
            """SELECT DISTINCT ht.slug, ht.title, ht.summary, ht.source_type
               FROM decklist_cards dc
               JOIN trip_card_refs tcr ON tcr.scryfall_id = dc.scryfall_id
               JOIN historical_trips ht ON ht.id = tcr.trip_id
               WHERE dc.decklist_id = ?""",
            (deck["id"],),
        ).fetchall()

        # Themes whose links match any card in the deck — group them
        theme_groups: dict[str, list[dict]] = {}
        for row in theme_hits:
            theme_groups.setdefault(row["theme_name"], []).append(dict(row))

    # Build the markdown report
    lines = [
        "# Cross-query demo: Hogaak Bridgevine ∩ MTGSLIDER themes",
        "",
        f"**Deck:** {deck['name']} ({deck['format']}, {deck['event_name']}, {deck['event_date']})",
        f"**Pilot:** {deck['pilot']}  ·  **Placement:** {deck['placement']}",
        f"**Source:** {deck['source_url']}",
        "",
        "This report demonstrates the integration between the decklist ingestion pipeline (Deckard plan D3/D6), the theme-curation database (slice 1), and the historical-trips research layer (Q22 new). The query joins three tables and surfaces which cards in this format-defining deck were already curated as instances of which themes.",
        "",
        f"**Total cards in deck:** {sum(r['quantity'] for r in cards)}  ·  **Distinct cards:** {len(cards)}",
        f"**Theme-database hits:** {len(theme_hits)} matches across {len(theme_groups)} themes",
        f"**Historical-trip references:** {len(trip_refs)}",
        "",
        "---",
        "",
        "## Theme matches",
        "",
    ]
    if not theme_groups:
        lines.append("*No theme matches.* The deck's cards have not been auto-curated into any themes in the current database — this is expected for a first demo run, since the bulk-generated themes (book, alchemy, etc.) target flavor concerns and Hogaak's cards are mostly mechanical-engine pieces. Build a `graveyard-engines` or `sacrifice-fodder` theme via the bulk runner and re-run this demo to see real cross-coverage.")
    else:
        for theme_name, rows in sorted(theme_groups.items()):
            lines.append(f"### {theme_name}")
            lines.append("")
            for r in rows:
                lines.append(f"- **{r['name']}** — `{r['include_status']}`")
            lines.append("")

    lines += [
        "---",
        "",
        "## Historical-trip references",
        "",
    ]
    if not trip_refs:
        lines.append("*No direct historical-trip references on this deck's cards yet.* As the etymology / biography / tradition corpus grows (see `writing/historical_trips/INDEX.md`), this section will populate.")
    else:
        for r in trip_refs:
            lines.append(f"- **{r['title']}** ({r['source_type']}) — {r['summary']}")
        lines.append("")

    lines += [
        "---",
        "",
        "## Full deck contents (for reference)",
        "",
        "| Qty | Card | Location |",
        "|---|---|---|",
    ]
    for r in cards:
        lines.append(f"| {r['quantity']} | {r['name']} | {r['location']} |")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
