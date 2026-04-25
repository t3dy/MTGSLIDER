# SCHOLARLYVALUES.md

An evidence-based audit of the user's scholarly values as observable across their humanities projects in `C:\Dev\`, with operational guidance for applying those values to MTG-historical-trip work — etymology cards, terminology rabbit holes, mechanic-history exposition, and slide content.

Every value below is anchored in a specific file in the user's own work. Where I couldn't find evidence, I haven't claimed the value. The ChatGPT chat archive is not currently accessible (per Q12 / Q20 — `SocialsDB` lacks a DB file, only fragmentary `GPT*.txt` exports exist), so the analysis is drawn from the project repos and their associated standards documents.

---

## Sources surveyed

| Project | Path | What it offers |
|---|---|---|
| AtalantaClaudiens | `C:\Dev\Claudiens\` | Most fully-articulated scholarly standards: `AFSTYLING.md`, `WRITING_TEMPLATES.md`, `SCHOLARSHIPREPORT.md`, ontology with provenance fields |
| EmeraldTablet (hermeticdb) | `C:\Dev\EmeraldTablet\` | Federated translation comparison; explicit "infrastructure hardening" phase discipline; `EMERALDTABLET.md` records translation provenance verse-by-verse |
| HP Marginalia (hypnerotomachia) | `C:\Dev\hypnerotomachia polyphili\` | Constraint-discipline: "Outward not deeper. Reality over design. No new specs without execution." Coverage tables of which copies, which scholars, which folios |
| Shakespeare Sonnets | `C:\Dev\Shakespeare\` | Same architecture; explicit Deckard plan (`SONNETSTUDYDECKARDANALYSIS.md`); 1609 Quarto text marked *sacred — never overwrite*; review pipeline DRAFT → REVIEWED → VERIFIED |
| alchemy_scryfall | `C:\Dev\alchemy_scryfall\` | Curated keyword lists drive theme construction; categorical organisation (Alchemists, Apothecaries, Chemists, etc.) |

The five share a remarkably consistent set of practices. They're not house style by accident — they're a methodology.

---

## The values, with evidence

### V1 — Provenance on every datum, always

**Evidence:** `Claudiens/docs/SYSTEM.md` defines three tracking fields on every generated row: `source_method` (DETERMINISTIC / LLM_ASSISTED / MANUAL), `confidence` (HIGH / MEDIUM / LOW), `review_status` (DRAFT / REVIEWED / VERIFIED). The same fields appear in `Shakespeare/docs/REVIEW_PIPELINE.md` and in EmeraldTablet's translation tables.

**The value:** No claim is asserted without a recorded origin. The reader can always trace any sentence in the published artifact back to a database row, then back to a source.

**Apply to MTG:** Every claim in an etymology card or speaker note must carry the same triple. The `mtg-historical-trip` etymology template already enforces `confidence:` in frontmatter — extend the convention to every paragraph that asserts a fact, not just card-level metadata. When the assertion is "MTG borrowed *scry* from John Dee", the source must be cited (Dee's *True & Faithful Relation*, Yates' *Occult Philosophy*) — not asserted as common knowledge.

### V2 — Source authorities are categorical, not generic

**Evidence:** `Claudiens/AFSTYLING.md` distinguishes HERMETIC, ALCHEMICAL, CLASSICAL, BIBLICAL, PATRISTIC, MOVEMENT, PUBLICATION, EDITION, SCHOLARSHIP, BIOGRAPHY — each with its own color badge and database type. `EmeraldTablet/EMERALDTABLET.md` separates Arabic vs Latin vulgate vs modern critical edition vs Bauer-Lindemann compilation as distinct provenance types. Shakespeare distinguishes 1609 Quarto from F1 from modern editorial.

**The value:** "Source" is too coarse. A claim cites a *kind* of source, and the kind matters — a patristic gloss is not the same kind of evidence as a tournament report or a Wizards designer column.

**Apply to MTG:** The MTG corpus has its own categorical types — WIZARDS_OFFICIAL (Mark Rosewater columns, set release notes, banlist announcements), SCRYFALL_DATA, TOURNAMENT_RECORD (MC IV coverage, MTGTop8 archive), STRATEGY_ARTICLE (CFB, MTGGoldfish editorial), FORUM_DISCUSSION (Reddit, Stack Exchange, EDHREC commentary), WIKI_REFERENCE (MTG Wiki), FAN_OPINION (personal blogs, YouTube transcripts). Add this taxonomy to MTGSLIDER's source layer. Treat WIZARDS_OFFICIAL the way Claudiens treats De Jong (canonical), TOURNAMENT_RECORD the way it treats primary alchemical texts (event-record), STRATEGY_ARTICLE the way it treats secondary scholarship (interpretive).

### V3 — One scholar's terminology is canonical; variants are noted, not silently merged

**Evidence:** `Claudiens/docs/WRITING_TEMPLATES.md`: *"Use De Jong's terminology as canonical. When scholars disagree, note the variant."* `EmeraldTablet/EMERALDTABLET.md` retains *all* 13 translations side-by-side rather than synthesising one canonical text. HP Marginalia has multiple `hp_copies` rows preserving each printed copy's idiosyncrasies separately.

**The value:** Variant terminology is *evidence*, not noise. Standardising it strips the historical record. A scholar's idiolect has authority within their corpus; it does not bind other corpora.

**Apply to MTG:** When MTG's mechanical vocabulary diverges from the historical source — "scry" in Dee means *gazing into a mirror to see hidden things*, in MTG it means *look at the top N cards and reorder* — preserve both senses, name the divergence, and don't pretend one is the "real" meaning. Similarly: when fan vocabulary diverges from official Wizards vocabulary ("midrange" was a fan term that Wizards eventually adopted; "tempo" is still mostly fan-side), record the divergence rather than smoothing it.

### V4 — Specificity over generality, with named entities and page numbers

**Evidence:** `Claudiens/docs/WRITING_TEMPLATES.md`: *"Avoid vague generalities like 'this emblem is significant' or 'the symbolism is complex.' Name concrete details — figures, objects, gestures, textual sources, page numbers."* Citations formatted as `(De Jong, p. 45)` or `(Tilton, ch. 3)`.

**The value:** Vague claims aren't refutable, so they aren't scholarly. The unit of authority is the *specific reference*.

**Apply to MTG:** "MTG borrows from alchemy" is the worst possible sentence. "Mark Rosewater's *Latest Developments* column dated 2014-04-21 introduces *scry* as evergreen, citing the Dee/Kelley scrying sessions from the *True & Faithful Relation* (Casaubon ed., 1659) as the design touchstone — though MTG's mechanical implementation diverges from Dee's practice in three named ways" is the goal sentence. Always: who, when, what page, what edition, what specific divergence. If the citation can't be pinned that tightly, mark the confidence as MEDIUM and hedge.

### V5 — Confidence language matches the actual confidence level

**Evidence:** `Claudiens/docs/WRITING_TEMPLATES.md`: *"HIGH confidence = declarative ('derives from,' 'identifies'). MEDIUM = hedging ('likely,' 'appears to,' 'De Jong suggests'). LOW = explicit uncertainty ('may represent,' 'the connection is speculative')."*

**The value:** Hedging is a precise tool, not politeness. Reading a paragraph should let the reader know how much weight to give each claim *from the prose alone*, without consulting the metadata.

**Apply to MTG:** The mtg-historical-trip etymology cards I've already written respect this — *scry* and *sorcery* use declarative language because the etymological chains are well-documented; *conjure*'s connection to medieval grimoire tradition is hedged because Mark Rosewater hasn't (to my knowledge) discussed the etymological choice on record. Maintain this discipline. When something is plausible but unsourced, say "the lexical fit is exact" rather than "MTG was citing the conjuror tradition."

### V6 — Original sources are sacred; never overwrite, never modernise without disclosure

**Evidence:** `Shakespeare/CLAUDE.md`: *"1609 Quarto text is sacred — never overwrite it."* HP Marginalia preserves the 1499 edition's typography, including marginalia marks. Claudiens preserves Maier's Latin text alongside English. EmeraldTablet preserves the Arabic and Latin vulgates separately rather than collapsing to a modern translation.

**The value:** The historical artifact is the *primary evidence*. Modernised versions are *commentary on it*. Confusing the two erodes the corpus.

**Apply to MTG:** Card text printed on a card is sacred — the version that appeared on the printed *Counterspell* in 1993 ("Counter target spell.") is not the same as the 2024 reprint's templated text ("Counter target spell."), even when the rules text is functionally identical, because the typography, frame, and layout carry historical information. When citing a card, cite the printing (set + collector number + year). When etymology touches printed-card-text, preserve the original wording. When discussing rules changes (e.g. how *protection from X* worked in 1996 vs 2024), preserve both rule states rather than smoothing.

### V7 — Architecture: SQLite source of truth, deterministic Python, no frameworks

**Evidence:** Identical architecture in Claudiens, EmeraldTablet, HP Marginalia, Shakespeare. SYSTEM.md docs all describe the same data flow: source files → SQLite → Python build script → static HTML → GitHub Pages. EmeraldTablet's `CLAUDE.md` is explicit: *"SQLite → Python pipeline → static HTML/CSS/JS → GitHub Pages. No frameworks, stdlib only."*

**The value:** Persistence over fashion. The user has chosen a stack that will run identically in twenty years. Frameworks rot; SQLite + Python do not.

**Apply to MTG:** MTGSLIDER follows the same pattern — already aligned. When the overlay-integration work (Q21) lands, keep the read API on the same SQLite handle rather than introducing a service layer. When the website grows (Q26), keep it static and framework-free. When tempted to add an embeddings store for "smart search", first try SQLite FTS5.

### V8 — Two-layer discipline: deterministic before LLM, with a wall between

**Evidence:** `Shakespeare/SONNETSTUDYDECKARDANALYSIS.md` is a Deckard plan; Claudiens has a `validate_enrichment.py` step between LLM-generated JSON and DB inserts; HP Marginalia has explicit `validation_architecture.md`. The pattern: parse structure deterministically, use LLM for semantic work, never write LLM output to the DB without validation.

**The value:** LLMs are useful for fuzzy semantic work and dangerous for structural claims. The two layers are kept separate by explicit gates.

**Apply to MTG:** This value is the spine of [DECKARD_BOUNDARY_PLAN.md](writing/DECKARD_BOUNDARY_PLAN.md) already. The MTGSLIDER schema's `review_status='unreviewed'` is the same wall as Claudiens' DRAFT status. Do not relax this discipline as the corpus grows — every additional source-type (forum scrapes, ChatGPT extractions, Q20 work) gets its own gate, never auto-promotion.

### V9 — Reality over design; outward, not deeper

**Evidence:** `hypnerotomachia polyphili/CLAUDE.md`: *"Outward not deeper. Surface existing data before adding more. Reality over design. Database beats documentation. Always. No new specs without execution. Build what's designed before designing more."*

**The value:** Discipline against the spec-creep pattern. The user explicitly names this as a guard against expanding a project's footprint beyond what's been built.

**Apply to MTG:** This is exactly what `PARKING_LOT.md` enforces in MTGSLIDER. When a new MTG terminology rabbit hole tempts you to design a fancy graph-traversal UI before any cards are written, write more cards first. The HP Marginalia stat — *431 matches surfaced before adding more matchers* — is the right shape: surface what exists before designing what doesn't.

### V10 — Document routing: name where to look, don't make people guess

**Evidence:** Claudiens has `DOCUMENTAIRTRAFFICCONTROL.md`, Shakespeare has the same, HP Marginalia has `SYSTEM.md` as the "read this first" entry. Each project's CLAUDE.md begins by naming the next-doc-to-read.

**The value:** Future readers (human or AI) should not have to grep to find the right starting point.

**Apply to MTG:** MTGSLIDER's `README.md` already does this. As the corpus grows, add a `MTGSLIDER/docs/INDEX.md` or similar that explicitly routes: *"researching a card's history? start with `writing/historical_trips/INDEX.md`. Want to know what's parked? `PARKING_LOT.md`. Want to know what was decided this session? `EXECUTION_LOG.md`."* The routing must always lead to a *file*, not a procedure.

### V11 — Reception history is first-class scholarship

**Evidence:** `Claudiens/SCHOLARSHIPREPORT.md` includes Walter Pagel's 1973 review of De Jong as a coverage source for emblems II, XIII, XVI, XXVIII, XLVIII — not as a footnote to De Jong but as its own row. HP Marginalia tracks dissertation references and annotator hands as first-class entities.

**The value:** A scholar's interpretation, the controversy around it, the later scholar's revision — all are evidence about the object being studied. Reception history is not auxiliary; it's part of the record.

**Apply to MTG:** Magic's reception history is *enormous* — every banlist controversy, every "is this card good?" debate, every retrospective on a banned format is reception. Don't reduce this to "what the cards do". Track who said what about a card and when. The Q21 overlay's `forum_summaries` table is the right shape; the Q18 competitive-history ingest creates the canon that reception comments on.

### V12 — AI-generated content is disclosed, not hidden

**Evidence:** `Claudiens/docs/WRITING_TEMPLATES.md` mandates a banner on every AI-drafted page: *"This content was drafted by an AI language model based on the scholarly sources in our corpus. It has not been reviewed by a human scholar. Citations are provided but should be verified against the original sources."*

**The value:** The reader has a right to know how a sentence was made. The disclosure is part of the artifact's authority structure — by acknowledging the LLM origin, the author preserves the reader's ability to weigh the claim.

**Apply to MTG:** Every LLM-assisted speaker note, slide-thesis paragraph, or historical-trip card body should carry an analogous banner — even on the published artifact, not just in the database. Currently MTGSLIDER's compiler `notes.py` produces speaker notes that *could* be mistaken for human-written; add a small "AI-assisted, sources at [link]" footer to compiler-generated notes by default.

### V13 — Phase discipline; status logged at the end of every session

**Evidence:** `Claudiens/PHASESTATUS.md`, `EmeraldTablet/PHASESTATUS.md`, `Shakespeare/PHASESTATUS.md` — same discipline across projects. Each project knows what phase it's in (DRAFT, READY, BUILT, BLOCKED, ARCHIVED). EmeraldTablet's CLAUDE.md is explicit: *"INFRASTRUCTURE HARDENING / CORPUS STRUCTURING. The project has enough corpus material. Collection is no longer the bottleneck."*

**The value:** A project should know what it's doing right now. Skipping phases or working in two phases at once produces incoherent state.

**Apply to MTG:** MTGSLIDER currently lacks an explicit `PHASESTATUS.md` (the closest is `ROADMAP.md` and the `EXECUTION_LOG.md`). Add one. As the etymology corpus grows, the project's phase will shift from "build the pipeline" to "populate the corpus" to "review and publish" — name the current phase explicitly and refuse to do work appropriate to a different phase without re-scoping.

### V14 — Restraint in synthesis; the scholar names what scholars argue, not what "is true"

**Evidence:** `Claudiens/docs/WRITING_TEMPLATES.md`: *"Always attribute interpretations to their scholar. 'De Jong identifies...' not 'The emblem represents...' Write about what scholars argue, not what the emblem 'means' in the abstract."*

**The value:** Scholarly humility is structural, not rhetorical. The artifact is what it is; what it *means* is always somebody's reading.

**Apply to MTG:** "*Goblin sacrifice mechanics enact the pharmakos figure*" is bad. "*Walter Burkert's reading of the pharmakos in Homo Necans (1972) provides one frame for thinking about Goblin sacrifice mechanics — the disposable body whose ritual destruction stabilises the larger system*" is good. The first sentence makes a claim about MTG; the second names a *reading* of MTG. Most of the writing in `writing/10_representative_themes.md` already does this; maintain the discipline as the corpus grows.

### V15 — Audit before extending; failure is logged, not papered over

**Evidence:** `hypnerotomachia polyphili/AUDIT_REPORT.md` and `Claudiens/SYSTEM_AUDIT.md` exist as recurring artifacts. The user runs `/plan-runciter-audit` and `/failure-audit` skills as ongoing practice, not crisis response.

**The value:** Things that don't work get named, not silently dropped. The audit log is the project's memory of its mistakes.

**Apply to MTG:** When an etymology card turns out to be wrong (better source surfaces, MTG retroactively releases a designer interview that contradicts a guess), record the change with provenance — don't silently rewrite. Add an `audits/` directory or extend `EXECUTION_LOG.md` with explicit retraction notes (the Q24/Q25 Attila pattern in conversation_log/ is the right shape).

---

## How these compose into "doing a rabbit hole on MTG terminology"

When you (or an AI agent) rabbit-hole on an MTG term — *cantrip*, *prowess*, *dredge*, whatever — the values above prescribe the following workflow:

1. **Frame the rabbit hole** as a research card slot in `writing/historical_trips/etymology/<term>.md`. The skill template already enforces structure — fill in the source-language chain (V3, V4), period definitions (V4), MTG use (V4).
2. **Cite specifically.** Every period definition gets a source. Every claim about MTG's use gets a card name + set + year. If you can't cite, hedge (V5) or omit.
3. **Categorise sources** (V2). When you cite Mark Rosewater, label it `WIZARDS_OFFICIAL`. When you cite a forum post, label it `FORUM_DISCUSSION` and note the date. When you cite Frances Yates, label it `SCHOLARSHIP`.
4. **Preserve variants** (V3). When MTG's *cantrip* differs from the D&D ancestor differs from the medieval *carmen* origin, name all three. Don't collapse to one canonical sense.
5. **Mark provenance** (V1) and **disclose AI assistance** (V12) on the published artifact, not just in the database.
6. **Hedge correctly** (V5). The lexical fit between MTG's *conjure* and the medieval grimoire tradition is *exact* (declarative). The claim that Wizards designers were *citing* the tradition when they coined the keyword is *speculative* (hedge).
7. **Don't over-synthesise** (V14). Name the figure who would have read the connection (Burkert, Yates, Eliade), don't claim the connection as fact-about-MTG.
8. **Surface before extending** (V9). Before designing a fancy term-relationship UI, write 20 etymology cards. Before writing 100, review the first 5 with the user.
9. **Phase the work** (V13). "Generating cards" and "reviewing cards" and "publishing cards" are different phases. Don't do them in the same pass.
10. **Audit retractions** (V15). When better evidence surfaces, log the retraction; don't silently rewrite the card.

---

## Where MTGSLIDER currently meets these values, and where it doesn't

| Value | MTGSLIDER status |
|---|---|
| V1 provenance | **Strong.** Schema has `confidence` + `review_status` + `source_url` on every claim-bearing table. |
| V2 categorical sources | **Weak.** No source-type taxonomy yet. Recommend adding `mtg_source_types` table with the 7-type vocabulary above. |
| V3 variant terminology | **Weak.** No `term_variants` or `archetype_aliases` table yet. Recommend adding when the corpus warrants. |
| V4 specificity | **Strong in 5 etymology cards.** As the corpus grows, enforce in review. |
| V5 confidence language | **Strong in cards.** Should also be enforced in compiler speaker notes (currently `notes.py` doesn't differentiate confidence). |
| V6 sacred sources | **Weak.** Card text in `cards.oracle_text` is current Scryfall — historical card text (e.g. Alpha *Counterspell* with the original wording) isn't preserved. Add a `card_printings_text` table for historical wordings if it ever matters. |
| V7 architecture | **Strong.** SQLite + Python + static HTML, no frameworks. Aligned. |
| V8 deterministic-before-LLM | **Strong.** Deckard plan locks this in. |
| V9 reality over design | **Strong.** PARKING_LOT.md does the work. |
| V10 document routing | **Adequate.** README.md routes well; could add a docs/INDEX.md when the docs grow. |
| V11 reception history | **Weak.** Forum summaries and competitive history are parked. When they land, treat them as first-class. |
| V12 AI disclosure | **Weak.** No banner on compiler-generated speaker notes or slide content. Recommend adding. |
| V13 phase discipline | **Weak.** No PHASESTATUS.md. Recommend adding. |
| V14 attributive synthesis | **Strong in writing layer.** As the corpus grows, enforce in review. |
| V15 audit before extending | **Adequate.** EXECUTION_LOG.md is the right shape; no formal audits/ yet. |

**Highest-leverage next-steps to align further:** add (a) a categorical `mtg_source_types` taxonomy, (b) AI-disclosure footers on compiler speaker notes, (c) a `MTGSLIDER/PHASESTATUS.md`. None are large; all reinforce values the user has already chosen elsewhere.
