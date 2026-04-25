# MTGSLIDER

Magic: The Gathering thematic research → curated card list → slideshow pipeline.

**Slice 1 scope:** Themes only (alchemists, books, lab furniture, dreams, ...). Archetype studies, format-historical questions, and saved Scryfall queries are explicitly deferred — see `REFRAME_NOTES.md`.

## Quick start

```bash
pip install -r requirements.txt
python -m mtgslider theme create "alchemists"
python -m mtgslider theme find-cards "alchemists" --query 't:creature o:alchemist'
python -m mtgslider theme list-cards "alchemists"
python -m mtgslider theme mark "alchemists" "Laboratory Maniac" --status include
python -m mtgslider theme fetch-images "alchemists" --variant normal
python -m mtgslider theme packet "alchemists"
python -m mtgslider slides build "alchemists" --backend v1
python -m mtgslider slides build "alchemists" --backend compiler
```

Outputs land in `themes/<slug>/` and `themes/<slug>/out/`.

## Architecture

```
src/mtgslider/
  scryfall.py          Scryfall API client (cached, rate-limited)
  images.py            Image downloader (provenance recorded)
  db.py                SQLite connection + migrations
  schema.sql           Theme schema (themes, theme_card_links, cards, images, sources)
  themes.py            Theme service: create/find/mark/list
  packet.py            Theme packet exporter (JSON + Markdown)
  cli.py               argparse-based CLI surface
  slideshow/
    v1_template/       Template-driven .pptx generator (Spec Dump 1)
    compiler/          Presentation compiler architecture (Spec Dump 4) — stub
```

The slideshow has **two backends** intentionally:
- `v1_template/` — fast, deterministic, ships now. Limited to a fixed slide-type set.
- `compiler/` — semantic slide types + layout registry + style presets. Stub-level today; iterate as needs become concrete.

Both consume the same theme packet — picking a backend is an output choice, not a research choice.

## What this does NOT do

- No LLM calls. Card selection, slide content, and packet text are all deterministic from your manual review and Scryfall data.
- No web scraping. Evidence ingestion (articles, decklists, B&R timeline) is parked.
- No archetype tracking. A "Tempo Merfolk" study needs decklist parsing + B&R timeline + format taxonomy and is out of scope for slice 1.
- No live banned-list lookup. Scryfall's `legalities` field is what we have.

## Files & docs

- `PARKING_LOT.md` — all 30+ subsystems and the architectural reframe, parked verbatim.
- `REFRAME_NOTES.md` — the topic→theme decision, with the four research-object types we explicitly chose not to unify.
- `ROADMAP.md` — what slice 2 might be, and the prerequisites it would need.
