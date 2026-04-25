# Q07 — Build authorization with project folder name

## Verbatim user input

> use your judgement and get building. Use different subfolders for different versions if we have two viable approaches that are different enough to be worth building out and trying. Create a project folder C:\Dev\MTGSLIDER

## How I interpreted it

Three explicit instructions:
1. Project folder name is `MTGSLIDER` (not the `mtg-research` scratch folder I created during planning)
2. Use my judgement — skip further planning ceremony, ship a working slice
3. Where two viable approaches exist (and only there), build both as alternatives

Decided slice 1 = **Themes** (per the reframe), and the only place two viable approaches genuinely exist is the slideshow backend (Spec Dump 1 template-driven vs Spec Dump 4 compiler). Built both as `slideshow/v1_template/` and `slideshow/compiler/`, sharing one foundation.

## What I built

Full slice-1 vertical: [MTGSLIDER/](../) with
- Scryfall service (cached, rate-limited, double-faced support)
- Image pipeline with provenance
- SQLite schema + theme service (create/find-cards/mark/list/fetch-images)
- Packet exporter (JSON + Markdown)
- argparse CLI (`mtgslider theme …`, `mtgslider slides build …`)
- v1_template slideshow generator
- Compiler stub: semantic slide types + layout registry + 3 style presets + narrative planner + validation
- 20 mocked tests, all passing
- `README.md`, `REFRAME_NOTES.md` (the topic→theme decision), `ROADMAP.md`, `PARKING_LOT.md`
- Smoke-tested live on "Alchemists" theme — 4 .pptx outputs with embedded card images

## What I deferred

All of slice 2 (archetype studies, format questions, manual evidence ingestion, static site, review dashboard, etc.) per the parked roadmap.
