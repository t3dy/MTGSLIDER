# DECKARD_BOUNDARY_PLAN.md

A boundary map for the proposed MTGSLIDER extension that triangulates magical/alchemical scholarship against MTG card vocabulary. Deckard distinguishes deterministic tasks from probabilistic ones. The plan names where AI work and Python-+-cited-source work meet, what artifacts get created at each boundary, and — most importantly — what NOT to use AI for.

This document does not prescribe implementation steps. Slice planning happens via `/plan-runciter-slice`. This is the architecture layer that any slice must respect.

---

## DETERMINISTIC TASKS (use Python + cited sources, not LLM)

### D1. Card data ingestion (Scryfall)
**Why deterministic:** Scryfall is a structured API. Card names, oracle text, type lines, mana costs, legalities, image URIs, set codes, collector numbers, prices, artist credits — all are typed fields with documented schemas. There is nothing for an LLM to interpret here.
**Artifact:** `cards` table (already exists in `MTGSLIDER/src/mtgslider/schema.sql`); `cache/scryfall/*.json` for full payload preservation.
**Existing implementation:** `src/mtgslider/scryfall.py` (rate-limited, cached).

### D2. Card image download
**Why deterministic:** HTTP GET of a known URL to a local path. Provenance fields (URL, timestamp, face, variant) are mechanical metadata.
**Artifact:** `theme_card_images` table; physical files under `themes/<slug>/images/`.

### D3. Decklist parsing
**Why deterministic:** Decklist text formats (MTGTop8 copy-paste, plain text "4 Counterspell" / sideboard separator, MTGO `.dek` XML, Arena export) are regular grammars. Card-name fuzzy lookup against Scryfall handles spelling drift; the structural parsing itself is regex/state-machine work.
**Artifact:** new `decklists`, `decklist_cards`, `tournament_results` tables. **DO NOT** ask an LLM to parse a decklist — every word is a card name lookup, and an LLM hallucinating "Lightning Bolt" when the user typed "Lightening Strike" is the precise failure mode this boundary exists to prevent.

### D4. Format legality at a point in time
**Why deterministic:** Legality is a function of (card printing date, format release date, banned-list timeline). Each is a dated record in a structured source. Scryfall gives current legality; historical legality requires a local B&R timeline (parked in `PARKING_LOT.md` Appendix B).
**Artifact:** `format_legality_events` table; `legality_at(card, format, date)` query function.

### D5. Tournament-result and decklist provenance
**Why deterministic:** Event name, date, format, placement, decklist-author, source URL — all are typed fields scrapable from the source pages with deterministic parsers. Provenance (URL + retrieval timestamp + parser version) is metadata.
**Artifact:** `tournament_results` table with `source_url`, `retrieved_at`, `parser_version` columns.

### D6. Set membership ("which cards are in this archetype's defining deck")
**Why deterministic:** Once a decklist is parsed (D3), "Hogaak Bridgevine 2019 Modern" is a fixed list of 75 cards. Membership queries are SQL joins. The LLM cannot improve on this.
**Artifact:** SQL queries against `decklist_cards`. Example: `SELECT cards.* FROM decklist_cards JOIN themes ON … WHERE decklist_id = 'hogaak-bridgevine-mc-barcelona-2019'`.

### D7. Vocabulary surface extraction from MTG cards
**Why deterministic:** Building the *initial* vocabulary surface — the set of words and phrases that appear on card names, type lines, and oracle text — is a tokeniser + frequency counter, not an LLM task. Lemmatisation can use spaCy or NLTK locally; no model API call needed.
**Artifact:** `mtg_vocabulary` table with `(token, lemma, frequency, sample_card_ids)`.

### D8. Federated entity reads
**Why deterministic:** Reading the `entities` table from each scholarly database (`Claudiens/`, `EmeraldTablet/`, etc., per `CONTEXT_ENGINEERING.md`) is SQL. SQLite FTS5 search over the `summary` column is SQL. No LLM call belongs here.
**Artifact:** `federated_reader.py` (~150 lines, parked).

### D9. Provenance and source-attribution metadata
**Why deterministic:** Every claim in the system carries `(source_db, source_id_or_url, retrieved_at, confidence, review_status)`. These are typed columns on the relevant rows. Generating these is mechanical.
**Artifact:** Provenance columns added to every claim-bearing table. Validation: row-insert triggers reject claims with NULL provenance.

### D10. Memory / documentation file maintenance
**Why deterministic:** Updating `MEMORY.md`, `PARKING_LOT.md`, `conversation_log/Q##_*.md`, `briefing.md` files — the file writes themselves are deterministic. The *content* may have probabilistic origin (see P2, P5), but the convention enforcement (file paths, frontmatter shape, naming `Q17`, `Q18`, …) is mechanical and should be a script or hook, not an LLM judgement call each time.
**Artifact:** A small `tools/log_query.py` could be built that takes a query, an interpretation, and a list of artifacts, and writes the next-numbered Q##_*.md file. (Parked — currently done by Claude as a manual convention.)

---

## PROBABILISTIC TASKS (LLM appropriate)

### P1. Concept-to-vocabulary mapping (the triangulation core)
**Why probabilistic:** "Does the alchemical concept *coniunctio* (union of opposites) map to MTG cards involving fusion, transformation, two-card combos, or pairings?" — this is fuzzy semantic mapping. There is no SQL query that produces it. An LLM with both vocabularies in context can propose candidate mappings.
**Validation:** every proposed mapping enters a `concept_card_mappings` table with `confidence='medium'` and `review_status='unreviewed'`. The user reviews and either promotes to `confidence='high'`/`review_status='reviewed'` or rejects. **Unreviewed mappings never appear in published artifacts** — they only feed the review UI.

### P2. Scholarly bridging prose (speaker notes, slide thesis text, essay paragraphs)
**Why probabilistic:** Writing prose that connects "Goblin sacrifice mechanics" to "the *pharmakos* in Walter Burkert's *Homo Necans*" is creative writing within a scholarly register. The user has already demonstrated they want this kind of writing (`writing/10_representative_themes.md`).
**Validation:** all prose carries `source_method='LLM_ASSISTED'`, `review_status='DRAFT'`. Citations within the prose must reference real entries in the federated entities layer (D8) — if a citation has no matching entity, the prose is rejected. **Prose with unresolved citations never gets written to a published artifact.**

### P3. Etymology cards (the `mtg-historical-trip` skill's main output)
**Why probabilistic:** Period definitions, semantic-shift narratives, attribution to source traditions — these draw on training-data knowledge that is *probably* correct but not guaranteed. The OED is paywalled and not directly queryable.
**Validation:** every claim in an etymology card carries an explicit `confidence` (high/medium/low) and a citation. Hedging language ("appears", "likely") is required for medium-confidence claims. The skill template enforces this. The user can verify against the actual OED if subscription access is available; the skill's output is *useful but not authoritative* and is marked as such.

### P4. Theme membership proposals (which cards belong to a theme)
**Why probabilistic:** "Is *Whispering Madness* a 'Books in Magic' card?" — the name, art, and flavor text taken together are a judgement call. Scryfall queries narrow the candidate set deterministically (D7); the LLM proposes which candidates are *exemplars*, *includes*, *uncertain*, or *excludes*.
**Validation:** the existing MTGSLIDER `theme_card_links.review_status` field is exactly this validation layer. Auto-curated links land as `unreviewed` and `confidence=0.5`. The user's `mark` command (or a future review UI) is the promotion mechanism. **No card gets `confidence>=0.8` or `review_status='reviewed'` without a human action.**

### P5. Forum-content summarisation
**Why probabilistic:** A 200-comment Reddit thread on *Hogaak* contains opinions, tournament reports, anecdotes, and noise. Summarising "what the community thought about this card during its dominance" is exactly the kind of NL synthesis where LLMs are useful and parsers are not.
**Validation:** the summary carries `source_url`, `retrieved_at`, `model_used`, `summary_method='LLM'`. Quoted claims within the summary must include the comment author handle and timestamp where extractable; otherwise they are paraphrases marked as such. **No forum claim is asserted as fact** — claims are framed as "according to [forum thread X], some users argued Y".

### P6. Cross-database concept linking
**Why probabilistic:** Recognising that Claudiens' "*solutio*" and EmeraldTablet's "*dissolutio*" and a hypothetical alchemy_scryfall entry on "dissolution" are the same concept under variant names is fuzzy matching across small specialised vocabularies. SQL `LIKE` would miss it; embeddings would over-match. An LLM with both records in context can answer well.
**Validation:** proposed cross-links go to a `concept_aliases` table with `proposed_by='LLM'`, `review_status='unreviewed'`. The user confirms or rejects. **The user's terminology in each source database is preserved** — aliases never overwrite canonical names.

---

## VALIDATION LAYERS (where LLM output enters deterministic systems)

### V1. The "draft → reviewed" wall
Every LLM-generated artifact lands as `review_status='unreviewed'` or `review_status='DRAFT'`. Every published artifact (slide deck, essay, static site page) reads ONLY from rows where `review_status='reviewed'`. This is a SQL `WHERE` clause in every query that produces a published artifact, enforced by code review of the build scripts.
**Implementation hint:** make the publishing scripts refuse to render slides whose card links or notes are in unreviewed state, with an explicit override flag for "preview" runs.

### V2. The "citation must resolve" wall
LLM-written prose (P2, P5) with citations is parsed for citation tokens (e.g. `[entity:claudiens:source-authority:turba]`). Each token is looked up in the federated entities layer (D8). Unresolved citations cause the prose to fail validation and land in a `drafts/` directory rather than the canonical output location.
**Implementation hint:** the `mtg-historical-trip` skill's `Wire-in commands` section already follows this pattern.

### V3. The "no claim without provenance" wall
Database triggers (or Python validators on insert) reject any row in a claim-bearing table where `source_db`, `source_id_or_url`, or `retrieved_at` is NULL. This catches the "LLM made up a fact and wrote it directly to the DB" failure mode.
**Implementation hint:** SQLite triggers are sufficient; no need for an ORM.

### V4. The "scrape vs cite" wall
Forum content has two modes: (a) **scrape**, where the parser extracts structured fields (post_id, author, timestamp, body) and LLM summarisation operates on the scraped body — full provenance preserved; (b) **cite**, where the system stores only the URL and human-readable title, no body extracted. Mode (b) is the default for ToS-restricted sources. The summary in mode (b) is *the user's note* about why the link matters, not an LLM summary of unread content.
**Implementation hint:** a `forum_sources` table with a `mode` column ('scrape' or 'cite') and a NOT NULL constraint forbidding LLM-summary content when mode='cite'.

### V5. The "human is the curator" wall
Theme membership (P4) and concept-to-vocabulary mapping (P1) are *proposed* by the LLM but *promoted* by a human action. The promotion event is itself logged with timestamp + actor, so the provenance of the curated state is auditable.
**Implementation hint:** add a `curation_events` table that logs every `mark` / `approve` / `reject` action.

---

## BOUNDARY VIOLATIONS TO AVOID

### W1. WASTE — Asking an LLM to parse a decklist
Don't. A decklist is a structured document with a regular grammar. An LLM parsing "4 Counterspell\n3 Snapcaster Mage" is paying for token-by-token inference of something a 20-line Python parser does perfectly. Worse, the LLM may hallucinate cards. **Decklist parsing is D3 — deterministic, full stop.**

### W2. WASTE — Asking an LLM to look up a card
Don't. Scryfall's API exists. The user has already paid for a Scryfall service module. An LLM that "remembers" *Lightning Bolt costs {R}* is slower, more expensive, and less correct than `scryfall.named("Lightning Bolt")`. **Card lookup is D1.**

### W3. WASTE — Asking an LLM to compute "which cards are in this deck"
Don't. Once D3 has populated `decklist_cards`, the answer is a SQL query. Asking the LLM is asking it to recall facts that the database already holds correctly.

### W4. RISK — Asking deterministic code to decide whether a card "fits a theme"
Don't write a hardcoded scoring function that says "if oracle text contains 'graveyard' then theme='necromancy'". That is the pre-Deckard era of MTG search engines and they were terrible. Theme membership is P4 — the LLM proposes, the human curates, the deterministic layer stores and queries the result.

### W5. RISK — Hardcoding which forums are "safe"
The list of safe sources changes (sites change ToS, forums die, new ones emerge). A hardcoded enum is brittle. Instead, maintain a `forum_sources` table where each row carries `tos_review_date`, `mode` (scrape/cite), `last_verified_at`, and a free-text `notes` column. Adding or removing a source is a row-edit, not a code change. The *judgement* about whether to scrape or cite is human; the *enforcement* is deterministic.

### W6. DANGER — LLM output flowing directly into a published artifact without review
Don't ever build a pipeline where Claude writes a paragraph and the same script publishes it to the website / .pptx / shared document. The V1 "draft → reviewed" wall must always sit between LLM output and any published artifact. Slide decks built from `unreviewed` data are explicitly *preview only* — watermark them, and refuse to write them to the canonical output directory.

### W7. DANGER — Cross-database concept aliasing without review
Don't auto-merge concepts across Claudiens / EmeraldTablet / etc. The user's databases preserve genuinely different scholarly terminology, and silently unifying them strips the provenance that makes those databases valuable. Cross-links must be proposed (P6) and confirmed (V5).

### W8. WASTE — Re-asking an LLM the same question across sessions
Don't. Cache LLM outputs the same way `scryfall.py` caches API responses. The `mtg-historical-trip` skill should write its research cards to disk; subsequent invocations on the same source should read the cached card unless the user passes `--refresh`. This is the same `cache/scryfall/` pattern, applied to LLM work.

---

## ARTIFACTS PRODUCED AT EACH BOUNDARY

This is the artifact map — what gets created where, by whom, with what provenance.

| Boundary | Artifact | Producer | Provenance fields | Promotion path |
|---|---|---|---|---|
| D1 | `cards` row, `cache/scryfall/*.json` | Python (Scryfall API) | `fetched_at` | direct (canonical from start) |
| D3 | `decklists`, `decklist_cards` rows | Python (parser) | `source_url`, `retrieved_at`, `parser_version` | direct |
| D4 | `format_legality_events` row | Python (manual import or scraper) | `announcement_url`, `effective_date` | direct |
| D7 | `mtg_vocabulary` row | Python (tokeniser) | `corpus_snapshot_date` | direct |
| D8 | `entities` row in each project DB | per-project `seed_entities.py` | `source_db`, `source_id` | direct (canonical to its DB) |
| D9 | provenance columns on every claim row | trigger / validator | (the columns themselves) | n/a — gate, not artifact |
| P1 | `concept_card_mappings` row | LLM proposal | `proposed_by='LLM'`, `model_used`, `proposed_at`, `confidence='medium'` | human `mark reviewed` action |
| P2 | speaker note / slide prose / essay paragraph | LLM | `source_method='LLM_ASSISTED'`, `review_status='DRAFT'`, `citations[]` | human review writes `review_status='reviewed'` |
| P3 | etymology / biography / tradition card under `writing/historical_trips/` | `mtg-historical-trip` skill | per-template `confidence` field | human edit promotes from `drafts/` to canonical location |
| P4 | `theme_card_links` row with `confidence=0.5`, `review_status='unreviewed'` | LLM-suggested or `find-cards` query | as above | `mtgslider theme mark` command |
| P5 | `forum_summaries` row | LLM operating on scraped body | `source_url`, `retrieved_at`, `model_used`, `summary_method='LLM'`, `quoted_authors[]` | human review |
| P6 | `concept_aliases` row | LLM proposal across federated entities | `proposed_by='LLM'`, `confidence='medium'` | human `mark reviewed` |
| V1–V5 | (no artifacts — these are gates) | enforcement code | n/a | n/a |
| memory | `MEMORY.md`, `feedback_*.md`, `project_*.md`, `conversation_log/Q##_*.md` | Claude (with human authorship via instruction) | implicit (the file is the artifact) | review on memory consolidation passes |
| docs | `briefing.md` per database, workspace `INDEX.md` | hand-written, refreshed by script | implicit | human edit |

---

## MEMORY AND DOCUMENTATION COMPOSITION (asked in scope #6)

The layers compose like this, from deepest to most session-local:

1. **Workspace `CLAUDE.md`** — invariant project profile and planning protocol. Read first, read always. Never auto-edited.
2. **Per-project `CLAUDE.md`** (e.g. `Claudiens/CLAUDE.md`, `MTGSLIDER/README.md`) — project-specific architecture, schema, and operating rules. Hand-edited; refreshed when architecture changes.
3. **Per-project `briefing.md`** (proposed in `CONTEXT_ENGINEERING.md`) — ~500-word pitch of what's in this project's data layer, written for an LLM about to query it cold. Hand-edited.
4. **Per-project ontology / schema docs** (`Claudiens/docs/ONTOLOGY.md`, `MTGSLIDER/src/mtgslider/schema.sql`) — structural reference. Auto-refreshed by `seed_entities.py` or equivalent.
5. **Project memory** (`~/.claude/projects/C--Dev/memory/project_*.md`) — what's happening on this project right now, what was decided, what was deferred. Updated when state changes meaningfully.
6. **Project `PARKING_LOT.md`** — the deferred-work log. Append-only. Items move to `ROADMAP.md` when scoped, never silently consumed.
7. **Project `conversation_log/Q##_*.md`** — per-query session audit. The freshest layer. Read for "what just happened in this session".
8. **Federated entities layer** (proposed) — programmatic cross-project surface for LLM tool calls. Doesn't replace the docs above; sits beneath them.

The right load order for an LLM picking up an MTGSLIDER task cold:
1. Workspace `CLAUDE.md`
2. `MTGSLIDER/README.md` + `MTGSLIDER/REFRAME_NOTES.md` + `MTGSLIDER/ROADMAP.md`
3. `MTGSLIDER/PARKING_LOT.md` (skim — what's already deferred)
4. `~/.claude/projects/C--Dev/memory/project_mtgslider.md` (what's the current state)
5. Last 1–3 entries of `MTGSLIDER/conversation_log/` (what happened most recently)
6. Specific schema/code files only as needed

For humans: same order, but also helpful is `writing/10_representative_themes.md` to see what the system is *for* in concrete terms.

---

## SUMMARY — THE BOUNDARY IN ONE SENTENCE

**Deterministic Python owns:** card data, decklist contents, format legality, vocabulary surfaces, provenance metadata, file/database I/O, and the federated entities reader.

**LLMs own:** semantic mapping between scholarly concepts and MTG vocabulary, scholarly bridging prose, etymology / biography / tradition research cards, theme-membership proposals, forum-content summarisation, and cross-database concept aliasing — all with explicit `confidence`, `review_status`, and citation requirements, and none of it published until a human promotes it.

**The wall between them is a SQL `WHERE review_status = 'reviewed'`.** Everything else is plumbing.

**The single most important rule:** no LLM-generated content reaches a published artifact (slide deck, website page, essay, .pptx output) without passing through the draft → reviewed promotion. This is the wall that makes the system trustworthy as scholarship.
