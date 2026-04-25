# ROADMAP

## Slice 1 (this build) — Themes

End-to-end loop: theme → Scryfall search → manual review → image fetch → packet → .pptx

**Acceptance:**
- Create a theme via CLI
- Stage Scryfall candidates
- Mark cards as include / exclude / exemplar / uncertain
- Fetch card images
- Export theme packet (JSON + Markdown) with provenance
- Generate .pptx via either backend (`v1` template or `compiler` stub)

## Slice 2 candidates (parked, NOT building yet)

Each requires `/plan-joe-chip-scope` and `/plan-runciter-slice` before starting.

### Slice 2a — Manual evidence ingestion for themes
Add `theme_sources` and `theme_claims` so a curator can attach articles, notes, and quoted claims to themes. Pure manual ingestion, no scraping.

### Slice 2b — Static site exporter
Theme packet → static HTML site mirroring the .pptx content. Same data, different render target. Should be cheap once the packet is stable.

### Slice 2c — Slideshow compiler maturation
Move `compiler/` from stub to first-class. Add layout registry entries beyond the stub, implement style presets (Sierkovitz / Rhystic / LLU), wire density controls and speaker-notes generation. Retire `v1_template` only when `compiler` covers everything `v1_template` does.

### Slice 2d — ArchetypeStudy type (NOT a theme refactor)
Add a second research-object type. Prerequisites that must land first:
- format/era taxonomy
- decklist parser
- banned/restricted timeline

This is the real test of the "shared interface, not shared schema" claim from `REFRAME_NOTES.md`. If it forces ugly compromises in the Theme code, the reframe is wrong and we should reconsider.

### Slice 2e — Review dashboard
Lightweight Flask app for reviewing theme cards visually. Currently the CLI is enough for slice 1, but a visual review surface becomes important once a theme has 100+ candidates.

## Things explicitly out of any near-term slice

- LLM-driven essay generation (per user preference for subscriptions over API calls; can be done in Claude Code or chat directly from a packet)
- Topic relationship graph
- Topic property extraction
- Multi-output modes (article, short-video) beyond .pptx
- Live presenter mode
- Source credibility scoring
- Claim conflict detector
- Argument graph linearization

All are in `PARKING_LOT.md` Appendices A–D.
