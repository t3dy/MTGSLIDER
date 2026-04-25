# EXECUTION_LOG.md

A running log of design decisions made during build phases that aren't already captured in `REFRAME_NOTES.md` (the topic→theme architectural pivot) or `PARKING_LOT.md` (deferred work). Entries are dated and named after the slice or task they belong to.

---

## 2026-04-24 — Slice 1 build

Decisions documented in [`REFRAME_NOTES.md`](REFRAME_NOTES.md) (the topic→theme reframe) and the project [`README.md`](README.md). Nothing additional to log here.

## 2026-04-24 — Slice 2c (compiler maturation)

Decisions documented in [`src/mtgslider/slideshow/compiler/README.md`](src/mtgslider/slideshow/compiler/README.md) (what's wired vs deferred) and in the regression-locking tests at [`tests/test_compiler_differentiation.py`](tests/test_compiler_differentiation.py) (which assert that the three style presets must produce structurally distinct outputs — these tests will fail if a future change collapses two presets back into the same shape).

## 2026-04-24 — Bulk run (98 / 100 themes)

Specs at [`tools/theme_specs.py`](tools/theme_specs.py); runner at [`tools/bulk_generate.py`](tools/bulk_generate.py); skip-log at [`themes/bulk_skipped.csv`](themes/bulk_skipped.csv). Two themes were skipped due to Scryfall query syntax errors (`Libraries as places`, `Ruins in Magic`); both are fixable by escaping single-quotes in the queries but were not blocking and were not fixed in the same pass.

## 2026-04-24 — Q22 build (this section is the centerpiece of this log)

Asked to "run em use your judgement" against the accumulated plans (Q17 scholarship-triangulation Deckard, Q18 competitive-history ingest, Q19 multilingual etymology, Q20 ChatGPT-archive Deckard, Q21 overlay integration). Did not attempt all five — picked the **smallest concrete vertical slice that exercises the unifying architecture across deterministic Python, LLM-authored content, and SQL cross-queries**.

### Decisions

**D-Q22-1: One slice, four artifacts.** Schema migration + 5 etymology cards + 1 famous deck + 1 cross-query report. Each artifact is independently useful; together they prove the architecture without over-committing token budget or implementation surface.

**D-Q22-2: Schema migration is additive only.** Three new tables (`historical_trips`, `trip_card_refs`, `decklists`, `decklist_cards`) plus indexes, all guarded with `IF NOT EXISTS`. No changes to existing tables, no breaking column changes, no triggers. Existing databases (the bulk-run output) get the new tables on next `connect()` call without disruption. All 29 existing tests pass after the migration.

**D-Q22-3: Etymology cards stored both on disk AND in SQLite.** The on-disk `.md` files (with YAML frontmatter) are the canonical authoring surface. The SQLite rows are derived — re-runnable from disk via `tools/ingest_historical_trips.py`. This pattern matches what `Claudiens/` does with its emblem manifest and makes future LLM-extension safer (re-runs don't lose human edits to the .md).

**D-Q22-4: 5 cards, not 10.** The 100-keyword target list (`writing/100_magical_keywords.md`) is the queue. Producing 5 cards demonstrates the format and seeds the database with enough material for the cross-query demo to be non-trivial. The remaining 95 are queued for batch generation in subsequent passes via the `mtg-historical-trip` skill. Quality (well-sourced, cited cards) over quantity (a hundred shallow stubs).

**D-Q22-5: Picked Hogaak Bridgevine over Caw-Blade for the deck demo.** Reasons: (a) more recent, more recoverable from public sources; (b) the archetype was banned within a month of its peak, making it a clean case of a format-defining deck; (c) heavy mechanical-engine cards (graveyard recursion, sacrifice fodder) that map to themes the bulk runner has already produced templates for; (d) 75-card list is straightforward to enter manually, no copy-paste of token-generators or planeswalker abilities to wrangle.

**D-Q22-6: Composite decklist, not a single pilot's list.** The Hogaak file uses `pilot: composite` rather than picking one player's MC IV top-8 list, because for *cross-query against thematic databases* the composite is more useful than any single deck's idiosyncratic land split or sideboard preference. The `pilot` field is honest about this. For tournament-record purposes the right move would be to ingest each player's specific list as its own row.

**D-Q22-7: Cross-query demo is a generator, not a static report.** [`tools/cross_query_demo.py`](tools/cross_query_demo.py) regenerates `writing/CROSS_QUERY_HOGAAK_DEMO.md` from the live database every run. The empty-state message ("no theme matches yet — build a `graveyard-engines` theme via the bulk runner") is a feature: it tells the user *what to do next* to get a populated report, rather than failing silently or pretending the architecture is broken.

**D-Q22-8: 1 unresolved card in the Hogaak ingest is acceptable.** The decklist parser saw a row "basics (Mountain x2, Forest, Swamp)" and could not fuzzy-match it to a single Scryfall card (because it isn't one). The ingester logs it and continues. The right fix is to expand the basics into separate rows in the source `.md`; the wrong fix is to make the parser smarter about basic-land rollups. Logging unresolved is the correct deterministic behaviour per the Deckard plan's V-3 ("no claim without provenance") wall.

### What was NOT done in Q22

- Etymology cards beyond the first 5 (queue is well-defined; producing more is a routine batch job).
- Decklists beyond Hogaak (every additional famous deck is one new `.md` file + one ingest run; no architectural work needed).
- The `historical_trips` ↔ specific Scryfall card linking is via `trip_card_refs` but the 5 cards generated reference *themes*, not specific Scryfall IDs (their `mtg_card_refs` frontmatter lists are empty). Linking to specific cards is the natural next pass.
- The Node-side overlay reader (Q21). The Python/SQLite half is now provable; the Node half is a separate project's slice.

---

## 2026-04-24 — Q26 build (browseable static website)

### Decisions

**D-Q26-1: Pure-Python generator, no framework.** Same discipline as `Claudiens/`: vanilla HTML/CSS, no npm, no build step beyond `python tools/build_site.py`. Output is `file://`-browseable AND ready for GitHub Pages deployment. ~620 lines of Python total ([`tools/build_site.py`](tools/build_site.py)) including a tiny in-house markdown converter (headings, lists, tables, code fences, links, bold, italic, inline code — covers the markdown subset this repo actually uses).

**D-Q26-2: Aesthetic borrowed from `Claudiens/AFSTYLING.md`.** Warm parchment background (`#f5f0e8`), dark brown serif body (`#2c2418`), burnt sienna accents (`#8b4513`). Same palette family as the user's other scholarly sites, so the project feels like part of a connected body of work rather than a generic dev artifact.

**D-Q26-3: Site IS committed, not gitignored.** The user asked for *a website I can use to browse* — committing the generated HTML means they can browse it immediately on github.com without running anything. It is deterministic and re-generated by `tools/build_site.py` whenever sources change.

**D-Q26-4: Code page links to GitHub blobs, not a local source-code viewer.** Building a local source-code highlighter would be substantial for marginal benefit — the GitHub blob view is already excellent. The code page is a navigable index pointing at github.com/t3dy/MTGSLIDER/blob/main/...

**D-Q26-5: Slideshow page links to .pptx files but does not preview them.** Browser-side .pptx preview would require a viewer library (PowerPoint web embed, or unzipping + parsing slide XML in JavaScript). Out-of-scope for the static-only stance. The user can click a row to download the .pptx and open it in Keynote / PowerPoint / LibreOffice.

### What was NOT done in Q26

- GitHub Pages deployment (one settings change on the repo + one workflow file). User can enable when ready.
- Search functionality. Premature for ~150 documents; FTS5-based local search is on the parking lot if the corpus grows.
- Card-image embedding in historical-trip pages. The data is in MTGSLIDER's DB; rendering is a follow-up pass.
- Live-data SQL views (e.g. "top themes by card count"). The site is currently a static artifact-browser; data-views would need either a build-time SQL pass or a local web server.
