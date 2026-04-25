# PARKING_LOT.md — MTG Research Project

> Hawthorne Abendsen wrote *The Grasshopper Lies Heavy* in safety. This is the same kind of safety. Ideas live here without disrupting current scope.

All ideas below were captured on **2026-04-24** during an initial brainstorming dump. None are in scope for the current build. The actual project scope has not yet been frozen — that requires `/plan-joe-chip-scope` and `/plan-runciter-slice` as separate, deliberate steps.

The four spec dumps are preserved verbatim in the appendices at the bottom of this file. The parking entries above each appendix summarize them in skill format.

---

## Parking Entries

### PARKED IDEA: MTG Research Pipeline — Foundation (Spec Dump 1)
**Description:** Ten foundational subsystems for a Magic: The Gathering research pipeline — Scryfall API service, card image retrieval, format-history SQLite schema, web research ingestion, decklist/tournament parser, thematic discovery engine, essay generator, slideshow generator (v1), review dashboard, orchestration CLI.
**Related project:** mtg-research (this directory; project not yet scoped)
**Complexity:** project (not session, not sprint — this is a multi-month system on its own)
**Prerequisites:** scope freeze via `/plan-joe-chip-scope`; vertical slice plan via `/plan-runciter-slice`; choose one initial theme as the proving ground; decide subscription vs API for any LLM-touching components per user's stated preference for subscriptions
**Status:** PARKED
**Date:** 2026-04-24
**Verbatim spec:** see Appendix A

---

### PARKED IDEA: MTG Research Pipeline — Domain Knowledge Layer (Spec Dump 2)
**Description:** Ten additional subsystems layering Magic-specific domain knowledge over the foundation — format/era taxonomy, banned/restricted tracker, archetype ontology, claim conflict detector, source credibility scoring, card-printing timeline service, legality validator, art/theme annotation, card cluster/comparison engine, static website exporter.
**Related project:** mtg-research
**Complexity:** project (every entry here is itself sprint-scale)
**Prerequisites:** foundation layer (Appendix A) must exist and have at least one working theme end-to-end; archetype ontology and format taxonomy probably need to come before conflict detector and legality validator regardless
**Status:** PARKED
**Date:** 2026-04-24
**Verbatim spec:** see Appendix B

---

### PARKED IDEA: Topic-First Architectural Reframe + Topic Intelligence Database (Spec Dump 3)
**Description:** Architectural pivot: topics (not cards) become the central first-class entity. Plus ten topic-intelligence subsystems — topic model, topic property extraction, topic relationship graph, topic-to-card linking, topic research packets, topic-specific evidence scoring, topic review UI, persistent topic memory across projects, topic comparison tools, topic-first workflow refactor.
**Related project:** mtg-research
**Complexity:** project — and this is also an architectural decision that should be pressure-tested with `/plan-mercer-reframe` before being adopted, because if accepted it changes the shape of everything in Appendices A and B
**Prerequisites:** `/plan-mercer-reframe` review of the topic-first hypothesis; only after reframe is accepted or rejected should any of these ten subsystems be sequenced
**Status:** PARKED
**Date:** 2026-04-24
**Verbatim spec:** see Appendix C

---

### PARKED IDEA: Slideshow Generator → Presentation Compiler (Spec Dump 4)
**Description:** Replaces the v1 slideshow generator (in Appendix A) with a presentation compiler architecture: semantic slide types as argument units, layout registry separating content from rendering, style presets (Sierkovitz/Rhystic/Limited Level Ups), narrative planner, density controls, speaker notes generation, evidence transparency modes, image selection strategy, section-level overrides, argument-graph linearization, multi-output targets (deck/short-video/article), iterative refinement loop, eventual presenter mode.
**Related project:** mtg-research
**Complexity:** project — by itself this is a substantial system
**Prerequisites:** the topic packet format must exist and be stable (depends on Appendix C decision); at least one working end-to-end theme exists in the v1 pipeline; explicitly supersedes the v1 slideshow generator from Appendix A item 8 — do not build both
**Status:** PARKED
**Date:** 2026-04-24
**Verbatim spec:** see Appendix D

---

### PARKED IDEA: Tweet-archive mining for topic generation
**Description:** User asked to generate 100 topics for "MTG's most magical keywords" by mining their tweets on historical magic and alchemy. Tweet archive is not currently accessible at `C:\Dev\SocialsDB` (metadata shows 1 twitter entry, no DB file). When archive becomes available, re-rank the keyword topic list (`MTGSLIDER/writing/100_magical_keywords.md`) by tweet attention or sentiment.
**Related project:** mtg-research / SocialsDB
**Complexity:** sprint
**Prerequisites:** locate or import a tweet archive into a queryable form; FTS5 index over tweet text; topic-extraction pass
**Status:** PARKED
**Date:** 2026-04-24

### PARKED IDEA: Artist-character types from Claudiens / EmeraldTablet / alchemy_scryfall
**Description:** Cross-reference MTG card artists and character archetypes (alchemists, magicians, scholars, artisans) against the user's scholarly databases. Goal: surface MTG cards whose flavor or art directly cites figures, motifs, or source-traditions documented in `Claudiens/`, `EmeraldTablet/`, `alchemy_scryfall/`, `renaissance magic/`. Blocked on a federated query layer across those SQLite files.
**Related project:** mtg-research + Claudiens + EmeraldTablet
**Complexity:** sprint
**Prerequisites:** federated read layer across the user's scholarly SQLite databases (see `MTGSLIDER/writing/CONTEXT_ENGINEERING.md`); shared provenance schema
**Status:** PARKED
**Date:** 2026-04-24

### PARKED IDEA: Literary/philosophical author tropes → MTG themes
**Description:** Given a named author, alchemist, magician, or natural philosopher (Borges, Paracelsus, John Dee, Ficino, Eliade), find MTG cards/themes that illustrate their characteristic tropes. The `mtg-historical-trip` skill (`source_type: biography`) already provides the per-source workflow; the parked piece is the *batch curation UI* — a way to maintain a reusable list of authors and re-run their trip cards as new MTG sets are released.
**Related project:** mtg-research
**Complexity:** session (batch UI) — sprint (with archival storage)
**Prerequisites:** `mtg-historical-trip` skill (DONE); a persistent author-list table in MTGSLIDER's SQLite schema
**Status:** PARKED
**Date:** 2026-04-24

### PARKED IDEA: Competitive Magic history ingest (all formats, all eras)
**Description:** Ingest the full competitive history of MTG into MTGSLIDER — tournament results, decklists, archetype membership, format-defining decks (Caw-Blade, Hogaak, Affinity, Combo Winter, etc.). Sources: MTGTop8, MTG Wiki archetype pages, Wizards' coverage articles, MTGGoldfish. Architecture is laid out in [DECKARD_BOUNDARY_PLAN.md](writing/DECKARD_BOUNDARY_PLAN.md) D3/D5/D6/V4 — deterministic parsing, scrape-vs-cite boundary per source, full provenance. Lets the system answer "which cards in the defining deck of archetype X were instances of theme Y."
**Related project:** mtg-research
**Complexity:** project (multi-week to multi-month)
**Prerequisites:** Decision on first slice (recommend ONE format + ONE recent year + ONE source as the proving slice); ToS review per source; `format/era taxonomy` and `B&R timeline` from PARKING_LOT Appendix B (or built fresh)
**Status:** PARKED
**Date:** 2026-04-24

### PARKED IDEA: Multilingual term-relationships browsing UI
**Description:** Website section over a `term_relationships` table where users can navigate from an English magical term (conjure, sorcery, alchemy, talisman) back through its source-language chain (Greek, Latin, Arabic, Hebrew, Old Norse, French, German), then sideways to cognates and cousins, with linguistic + cultural commentary. Data layer is in place: the `mtg-historical-trip` skill's etymology template now has `Source-language chain` and `Cognates and cousins` sections. UI is the parked piece.
**Related project:** mtg-research (website extension)
**Complexity:** sprint
**Prerequisites:** `historical_trips` table in MTGSLIDER schema; ~20+ etymology cards generated as a usable corpus; static-site generator (parked separately)
**Status:** PARKED
**Date:** 2026-04-24

### PARKED IDEA: ChatGPT chat-archive ingest for MTG project archaeology
**Description:** Ingest the user's ChatGPT chat history (OpenAI data export ZIP), extract MTG-related conversations, design ideas, and "desires", and federate the results into MTGSLIDER's context layer. Architecture in [DECKARD_BOUNDARY_PLAN_chatgpt_ingest.md](writing/DECKARD_BOUNDARY_PLAN_chatgpt_ingest.md). Critical wall: extracted desires never auto-promote to ROADMAP — they enter PARKING_LOT for normal scoping discipline.
**Related project:** SocialsDB-adjacent; new project at e.g. `C:\Dev\ChatGPTArchive\`
**Complexity:** project
**Prerequisites:** Locate or fetch a fresh OpenAI chat export; confirm format; decide on private-content gate threshold; pick first slice (likely: ingest archive, run keyword-relevance pass, do not invoke LLM extraction in slice 1)
**Status:** PARKED
**Date:** 2026-04-24

### PARKED IDEA: Live MTG Arena overlay integration with MTGDraftOverlay
**Description:** Integrate MTGSLIDER's curated content (themes, packets, historical-trip cards, multilingual etymology) with the existing `C:\Dev\MTGDraftOverlay\` Node.js project so that during MTG Arena gameplay (draft and constructed) the overlay can show transparent, toggleable commentary tabs alongside its existing 17Lands draft-rating panels. Full integration analysis at [writing/OVERLAY_INTEGRATION.md](writing/OVERLAY_INTEGRATION.md). Critical Deckard rule: NO LLM invocation in the live gameplay path — content is pre-computed offline, served deterministically at runtime.
**Related project:** MTGSLIDER + MTGDraftOverlay
**Complexity:** sprint (smallest viable slice = 5 hand-curated cards on a single new "Historical" tab in draft mode); project (full constructed-mode + full content corpus)
**Prerequisites:** `historical_trips` table in MTGSLIDER schema; ~5+ curated trip cards as proving content; Node-side SQLite handle (`better-sqlite3`); minimal MTGDraftOverlay extension to render a `CommentaryPanel`-shaped tab
**Status:** PARKED
**Date:** 2026-04-24

### PARKED IDEA: Federated context-engineering layer across user databases
**Description:** A unified query layer over Claudiens, EmeraldTablet, alchemy_scryfall, renaissance magic, MTGSLIDER, SocialsDB. Goal: enable cross-database queries like "which MTG cards have flavor that cites a concept also found in EmeraldTablet's hermetic concept index?" — without forcing a monolithic schema. Recommendation document at `MTGSLIDER/writing/CONTEXT_ENGINEERING.md` describes the proposed shape (federated SQLite + shared provenance schema + per-database read APIs). Building it is its own multi-week project.
**Related project:** workspace-level (spans many)
**Complexity:** project
**Prerequisites:** see CONTEXT_ENGINEERING.md
**Status:** PARKED
**Date:** 2026-04-24

---

## Scope Discipline Notes

- Total parked surface area: ~30 subsystems plus one architectural pivot plus one major rewrite of an unbuilt component.
- The v1 slideshow generator (Appendix A, item 8) is superseded by the presentation compiler (Appendix D). Do not build the v1 if the compiler reframe is accepted.
- The topic-first reframe (Appendix C) changes the shape of Appendices A and B. Resolve the reframe question before scoping any slice from A or B.
- A reasonable first vertical slice (when scoping happens) might be: Scryfall lookup → image fetch → minimal SQLite schema → manual theme curation → one .pptx export, on a single narrow theme. Everything else is deferred until that proves the loop.

---

## SCOPE WARNING

If the user tries to start working on any parked idea above without re-scoping:

> **SCOPE WARNING:** This idea is parked. To work on it, first re-freeze scope with `/plan-joe-chip-scope` to include it, or start it as a separate project.

---

# Appendix A — Spec Dump 1 (Verbatim)

## Build the Scryfall API service
Build a clean Scryfall API service module.

Scope:
- Search cards by name, oracle text, type line, color, commander identity, set, format legality, and art/theme keywords.
- Support exact lookup, fuzzy lookup, and paginated search.
- Return normalized card objects with:
  - name
  - mana_cost
  - type_line
  - oracle_text
  - colors
  - color_identity
  - legalities
  - set info
  - image_uris
  - artist
  - prices if available
  - Scryfall URI
- Handle double-faced cards correctly.
- Add caching so repeated searches do not hammer the API.
- Include rate-limit-safe request handling.
- Write tests using mocked API responses.

Do not build UI yet. This is only the data access layer.

## Build the card image retrieval pipeline
Build a card image retrieval and storage pipeline using the Scryfall service.

Features:
- Given a list of card names or Scryfall IDs, download the best available card images.
- Support normal, large, png, art_crop, and border_crop image variants.
- For double-faced cards, save both faces with deterministic filenames.
- Store image metadata in a local JSON or SQLite table.
- Avoid duplicate downloads.
- Record provenance:
  - Scryfall ID
  - image URL
  - download timestamp
  - card face
  - image type
- Add a CLI command:
  python tools/fetch_card_images.py --cards input/cards.json --variant large

Keep this independent from slideshow generation.

## Build the Magic format history research schema
Design and implement a research schema for Magic card historical importance.

Use SQLite.

Tables should cover:
- cards
- formats
- eras
- archetypes
- decklists
- tournament_results
- article_sources
- card_format_assessments
- claims
- citations

The key model is:
A card can be important in one format during one era for one reason, but irrelevant in another.

Each assessment needs:
- card_id
- format
- era/date range
- archetype if applicable
- importance rating
- role: staple, sideboard card, build-around, role-player, casual-only, fringe, banned/restricted, obsolete
- evidence summary
- citations
- confidence level
- review status

Do not scrape yet. Build schema, migration, seed data, and documentation.

## Build the web research ingestion module
Build a research ingestion module for gathering evidence about Magic cards from the web.

Scope:
- Accept search topics like:
  - "important zombie cards in Legacy"
  - "history of Counterspell in Pauper"
  - "best book-themed Magic cards"
- Generate structured research queries.
- Store discovered URLs, titles, snippets, source type, and retrieval date.
- Allow manual import of article text or notes.
- Extract candidate claims like:
  - card X was a staple in format Y
  - card X was banned in format Y
  - card X appeared in archetype Z
  - card X was mostly casual
- Every extracted claim must be linked to a source.
- Use review_status = unreviewed by default.

Do not make unsupported claims look verified.

## Build the decklist/tournament evidence parser
Build a parser for decklist and tournament evidence.

Inputs:
- MTGTop8-style copied text
- tournament decklist pages saved as HTML
- plain text decklists
- CSV exports

Outputs:
- normalized decklists
- card counts
- archetype labels if available
- format
- event name
- date
- placement
- source URL

Features:
- Detect mainboard vs sideboard.
- Normalize card names through Scryfall fuzzy lookup.
- Store parsed data in SQLite.
- Produce aggregate stats:
  - number of appearances per card
  - number of decks per archetype
  - sideboard-only vs mainboard use
  - date range of appearances

Keep this as evidence, not final interpretation.

## Build the thematic card discovery engine
Build a thematic discovery engine for finding Magic cards by theme.

Example themes:
- zombies
- books
- libraries
- scholars
- alchemy
- dreams
- masks
- insects
- ruins
- sea monsters

Search across:
- card name
- type line
- oracle text
- flavor text if available
- art tags if available
- manual tags
- Scryfall syntax queries

Output:
- ranked candidate cards
- reason for match
- matching field
- confidence
- image reference
- theme tags

Include a manual override layer so I can mark:
- include
- exclude
- uncertain
- exemplar

## Build the card evaluation essay generator
Build an essay planning module that turns researched cards into an organized Magic history essay.

Input:
- theme or topic
- selected cards
- format assessments
- citations
- images

Output:
- structured essay outline
- card-by-card sections
- format/era notes
- citations
- suggested slide titles
- image suggestions

Essay structure should support:
- introduction to the theme
- early history
- competitive history by format
- casual/Commander relevance
- notable design patterns
- conclusion

Do not hallucinate. If evidence is weak, write "uncertain" or "needs review."

## Build the slideshow generator
Build a slideshow generator for Magic card research outputs.

Input:
- essay outline JSON
- selected card image metadata
- card assessments
- citations

Output:
- PowerPoint .pptx

Slide types:
- title slide
- thesis/context slide
- card spotlight slide
- format history slide
- archetype slide
- comparison slide
- citation/source slide

Card spotlight slides should include:
- card image
- name
- format/era relevance
- short notes
- citation footer

Support layouts for:
- one card
- two cards
- four-card grid
- timeline slide

Keep generation deterministic and template-driven.

## Build the review dashboard
Build a lightweight local review dashboard.

Use static HTML or a small Flask app.

Purpose:
Review and correct research before generating essays or slides.

Views:
- cards by theme
- claims needing review
- cards missing images
- cards with conflicting assessments
- format history timeline
- source list
- slideshow preview queue

Actions:
- approve claim
- reject claim
- edit summary
- change confidence
- add manual note
- include/exclude card from final output

Do not overbuild. Prioritize fast correction and provenance visibility.

## Build the orchestration CLI
Build a top-level CLI that orchestrates the full Magic research pipeline.

Commands:
- mtg-research search-theme "zombies"
- mtg-research fetch-images --theme zombies
- mtg-research ingest-source --url URL
- mtg-research parse-decklist file.txt
- mtg-research assess-card "Gravecrawler" --format Modern
- mtg-research build-essay --theme zombies
- mtg-research build-slides --theme zombies
- mtg-research review-dashboard

Design rules:
- Each command should call service classes, not contain business logic.
- Every output should be written to a deterministic folder.
- Every generated artifact should include provenance.
- Never silently overwrite reviewed data.
- Add a README showing example workflows.

---

# Appendix B — Spec Dump 2 (Verbatim)

## Build the format/era taxonomy module
Build a controlled vocabulary module for Magic formats and eras.

Include:
- Standard
- Modern
- Legacy
- Vintage
- Pioneer
- Pauper
- Commander
- Limited
- Block Constructed
- Extended
- Premodern
- Old School

For each format, model:
- start date
- active/inactive status
- rotation behavior
- banned/restricted list URL field
- common evidence sources
- notes on interpretation

Also define eras:
- Alpha–Revised
- Early Type II
- Combo Winter
- Invasion/Odyssey era
- Mirrodin era
- Ravnica era
- Modern founding period
- FIRE design era
- Commander boom
- Arena era

Make the taxonomy editable, but do not let arbitrary strings leak into the database.

## Build the banned/restricted list tracker
Build a banned/restricted list tracker.

Scope:
- Store official banned/restricted events by format and date.
- Link affected cards to the announcement source.
- Track whether a card was banned, restricted, unbanned, or unrestricted.
- Support manual import first.
- Add fields for:
  - announcement date
  - effective date
  - format
  - card name
  - action
  - source URL
  - summary
  - confidence
  - review status

The goal is not live automation yet. The goal is reliable historical context for card evaluations.

## Build the archetype ontology
Build an archetype ontology for Magic deck history.

Model archetypes as first-class entities:
- Aggro
- Control
- Midrange
- Combo
- Tempo
- Prison
- Ramp
- Reanimator
- Tribal
- Aristocrats
- Burn
- Storm
- Dredge
- Affinity
- Delver
- Tron
- Jund
- Faeries
- Caw-Blade
- Zombies
- Elves
- Goblins
- Merfolk

Support parent/child archetypes:
- Tribal > Zombies
- Combo > Storm
- Aggro-Control > Delver
- Artifact Aggro > Affinity

Each archetype should have:
- description
- formats where relevant
- date range
- key cards
- source citations
- review status

Do not hard-code this into essay generation. Make it reusable data.

## Build the claim conflict detector
Build a claim conflict detector for Magic research.

Detect cases like:
- one source says a card was format-defining, another says fringe
- a card is marked legal during a period when it was banned
- a card is assigned to the wrong format era
- a card appears in an archetype before its print date
- decklist data contradicts an essay claim
- duplicate claims with different confidence levels

Output:
- conflict type
- affected card
- affected format/era
- conflicting claims
- source references
- suggested resolution
- severity

Do not auto-resolve conflicts. Write them to a review queue.

## Build the source credibility scoring layer
Build a source credibility layer for Magic research.

Classify sources as:
- official Wizards announcement
- Scryfall data
- tournament database
- decklist archive
- strategy article
- forum thread
- Reddit discussion
- wiki page
- personal blog
- YouTube transcript
- unknown

Each source should get:
- source_type
- authority_score
- date
- author if available
- URL
- title
- notes
- review status

Use the score only as a guide. Do not let it automatically turn claims into verified facts.

## Build the card-printing timeline service
Build a card printing timeline service using Scryfall data.

For any card, retrieve:
- first printing date
- all printings
- sets
- rarities
- reprints
- promo versions
- digital-only status
- commander/precon appearances if available
- image per printing

Use this to support:
- “when did this card enter the ecosystem?”
- “was this card available in this format at that time?”
- “which artwork should be used for this era?”

Expose as a service used by essays, slides, and validation.

## Build the legality validator
Build a legality validator.

Given:
- card
- format
- date or era

Return:
- legal
- banned
- restricted
- not yet printed
- rotated out
- unknown

Inputs:
- Scryfall legalities
- local banned/restricted timeline
- format taxonomy
- card printing timeline

Important:
Scryfall gives current legality. Historical legality must come from the local timeline and format rules.

Flag uncertain cases for review.

## Build the art/theme annotation module
Build an annotation module for card art and themes.

For each card or card face, allow manual annotations:
- visible objects
- creature type/theme
- setting
- mood
- symbolic motifs
- color palette notes
- composition notes
- relevance to chosen theme
- image quality
- slide suitability

Example:
For a “books in Magic” theme, mark cards that visibly show books, scrolls, libraries, scholars, desks, archives, or magical writing.

This should be human-reviewable. Do not pretend visual tags are certain unless manually confirmed.

## Build the card cluster/comparison engine
Build a comparison engine for grouping cards.

Support grouping by:
- mechanic
- creature type
- format role
- archetype
- era
- color identity
- mana value
- flavor theme
- art motif
- competitive importance
- casual/Commander relevance

Output clusters like:
- “Zombie recursive threats”
- “Zombie lords”
- “Graveyard engines”
- “Sideboard graveyard hate”
- “Bookish blue card draw”
- “Library-as-place cards”
- “Alchemy-themed artifacts”

Use this to generate essay sections and slideshow group slides.

## Build the static website exporter
Build a static website exporter for researched Magic topics.

Input:
- theme/topic project data
- essay markdown
- card images
- citations
- card assessments
- timelines

Output:
- static HTML/CSS/JS site

Pages:
- topic home
- card gallery
- format history
- archetype history
- sources
- review status page
- image credits

Requirements:
- no heavy framework
- deterministic build output
- local assets only after fetch step
- provenance visible
- uncertainty badges visible
- mobile-friendly card gallery

This should mirror the same data used for the slideshow, not create a separate content system.

---

# Appendix C — Spec Dump 3 (Verbatim)

> Prefixed by user with: "Yes. Make that a first-class topic intelligence database, not just a search log."
>
> Key abstraction: **Topic = any research target worth developing into cards, claims, images, essays, slides, or web pages.** Examples include alchemists, lab furniture, books, dreams, tempo merfolk, zombie archetypes in limited, black recursive one-drops, cards showing desks, graveyard engines in Pioneer.

## Build the topic model
Build a Topic Intelligence schema for the Magic research project.

A topic is any user-entered research subject, including:
- flavor theme: alchemists, books, dreams
- visual motif: lab furniture, desks, masks
- mechanical theme: sacrifice outlets, recursion, tempo
- archetype: Tempo Merfolk, Zombie Limited archetypes
- historical subject: Combo Winter, Caw-Blade
- format-specific question: Zombies in Limited, Merfolk in Modern

Create SQLite tables:
- topics
- topic_aliases
- topic_types
- topic_properties
- topic_card_links
- topic_source_links
- topic_claim_links
- topic_relationships
- topic_review_notes

Each topic should have:
- canonical_name
- slug
- topic_type
- short_description
- research_status
- confidence
- created_at
- updated_at
- review_status

Do not reduce topics to tags. Topics need their own durable identity.

## Build topic property extraction
Build a topic property extraction module.

Given a topic like "lab furniture", "alchemists", or "tempo merfolk", infer candidate properties worth researching.

Property examples:
For "alchemists":
- associated creature types
- color identity tendencies
- recurring mechanics
- art motifs
- notable cards
- historical formats
- related planes
- source traditions
- terminology variants

For "lab furniture":
- visible objects
- art crops
- card types likely to show it
- related motifs: books, bottles, instruments, desks, scrolls
- image suitability

For "tempo merfolk":
- format relevance
- key cards
- archetype role
- era range
- typical interaction package
- lords
- mana curve
- evidence sources

Store properties as typed records:
- property_name
- property_value
- property_type
- source
- confidence
- review_status

All inferred properties start as unreviewed.

## Build topic relationship graph
Build a topic relationship graph.

Topics can relate to other topics as:
- broader_than
- narrower_than
- overlaps_with
- visual_motif_of
- archetype_variant_of
- format_instance_of
- historically_related_to
- mechanically_related_to
- flavor_related_to
- contradicts
- alias_of

Examples:
- "lab furniture" overlaps_with "alchemy"
- "alchemists" flavor_related_to "artifacts"
- "tempo merfolk" archetype_variant_of "merfolk"
- "zombie archetypes in limited" format_instance_of "zombies"
- "recursive zombies" mechanically_related_to "graveyard recursion"

Implement graph queries:
- show related topics
- expand topic research scope
- find sibling topics
- find cards shared by two topics
- find topics with weak evidence

Keep this separate from the card database.

## Build topic-to-card linking
Build a topic-to-card linking service.

Given a topic, link candidate cards using:
- Scryfall search
- local card text
- type line
- flavor text
- manual art annotations
- existing claims
- decklist evidence
- manual includes/excludes

Each link should record:
- topic_id
- card_id
- link_reason
- link_type: name_match, type_match, oracle_match, flavor_match, art_match, archetype_evidence, manual
- confidence
- include_status: include, exclude, uncertain, exemplar
- review_status

A card can be linked to the same topic for multiple reasons.

Example:
"Laboratory Maniac" links to:
- lab furniture: weak visual/name relation
- alchemists/scholars: possible flavor relation
- alternate win conditions: strong mechanical relation

## Build topic research packets
Build a Topic Research Packet generator.

For any topic, output a JSON and Markdown packet containing:
- topic summary
- aliases
- related topics
- candidate cards
- exemplar cards
- uncertain cards
- excluded cards
- known format relevance
- visual motifs
- mechanical motifs
- unresolved questions
- sources
- claims needing review
- slideshow potential

This packet is the handoff format for essay generation, slide generation, and review.

Command:
python tools/build_topic_packet.py "tempo merfolk"

## Build topic-specific evidence scoring
Build evidence scoring for topic-card relationships.

Different topics need different evidence rules.

For flavor topics:
- name match is medium evidence
- flavor text is medium evidence
- art annotation is strong evidence
- oracle text may be weak or irrelevant

For archetype topics:
- decklist appearance is strong evidence
- strategy article mention is medium evidence
- creature type alone is weak evidence

For visual motif topics:
- manual art annotation is strong evidence
- card name is weak evidence
- art crop availability matters

For format-history topics:
- tournament/decklist evidence is strong
- current legality is not enough
- casual popularity is separate

Implement topic_type-specific scoring rules.

## Build the topic review UI
Build a review UI for topic intelligence.

Views:
- topic overview
- candidate cards
- topic properties
- related topics
- claims
- sources
- unresolved questions

Actions:
- approve/reject topic-card link
- mark card as exemplar
- edit property
- merge duplicate topics
- add alias
- create related topic
- mark topic ready for essay
- mark topic ready for slides

The UI must show uncertainty clearly.
Do not hide weak evidence.

## Build topic memory across projects
Build persistent topic memory.

If I research "alchemists" once, later projects should reuse that knowledge.

Requirements:
- Topic records persist independently of a single slideshow or essay.
- A topic can belong to many projects.
- A project can use many topics.
- Topic data should improve over time.
- Reviewed topic-card links should not be overwritten by new automated runs.
- New automated findings should be staged as candidates.

Add tables:
- projects
- project_topics
- topic_snapshots

Snapshots preserve what was known when a slideshow or essay was generated.

## Build topic comparison tools
Build topic comparison tools.

Commands:
- compare-topics "alchemy" "lab furniture"
- compare-topics "tempo merfolk" "aggro merfolk"
- compare-topics "zombies in limited" "zombies in commander"

Output:
- shared cards
- unique cards
- shared properties
- conflicting properties
- format differences
- era differences
- visual motif differences
- mechanical differences
- sources supporting each distinction

This should help generate more sophisticated essays instead of flat card lists.

## Build the topic-first workflow
Refactor the Magic research pipeline around topics.

The main workflow should be:

1. User enters topic.
2. System creates or retrieves topic record.
3. System expands aliases and related concepts.
4. System searches Scryfall.
5. System fetches images.
6. System searches/imports evidence.
7. System proposes topic properties.
8. User reviews candidates.
9. System builds topic packet.
10. System generates essay/slides/site from reviewed topic packet.

Add CLI:

mtg-topic create "alchemists"
mtg-topic expand "alchemists"
mtg-topic find-cards "lab furniture"
mtg-topic review "tempo merfolk"
mtg-topic packet "zombie archetypes in limited"
mtg-topic compare "alchemy" "books"

The important design rule: cards are not the center of the system; topics are. Cards, decklists, images, claims, and sources orbit the topic. This lets you build a reusable research memory instead of starting over every time.

---

# Appendix D — Spec Dump 4 (Verbatim)

> Treat the slideshow generator as a **presentation compiler**, not a template filler. It should transform a structured topic packet into a lecture-ready artifact with controllable rhetorical structure, visual density, and evidence framing.
>
> The design problem splits into three layers: (1) slide semantics, (2) layout/rendering, (3) creator control surface.

## 1) Slide semantics (what kinds of slides exist)

You need a richer ontology than "title + bullets." Model slides as **argument units**.

Core slide types:
- **Thesis / framing** — establishes scope, claim, or question
- **Definition / taxonomy** — what counts as "zombie," "tempo," etc.
- **Historical phase** — era-based segmentation (e.g., Onslaught Zombies vs Innistrad Zombies)
- **Card spotlight** — one card, tightly framed claim
- **Cluster / comparison** — groups (lords vs recursive threats vs payoffs)
- **Deck archetype** — representative list + role explanation
- **Mechanics breakdown** — how something actually works (tempo, recursion loops)
- **Data / evidence** — tournament frequency, winrate, appearance counts
- **Visual motif** — art/theme slides (important for Rhystic-style content)
- **Counterpoint / mythbusting** — "this card is overrated," "this archetype wasn't actually dominant"
- **Transition** — bridges between sections
- **Conclusion / synthesis**

Claude prompt:

    Extend the slideshow generator to support semantic slide types.

    Each slide must declare:
    - slide_type
    - rhetorical_role
    - required_fields
    - optional_fields

    Do not render yet. Only define the schema and validation rules.

## 2) Layout system (how slides look)

Separate **content from layout completely**.

Each slide type can map to multiple layouts:
- single-image focus (card or art)
- split (image + text)
- grid (2–6 cards)
- timeline (era progression)
- comparison (left/right)
- data chart (bar, line)
- minimal (one sentence, big font)
- dense (for handout-style decks)

Claude prompt:

    Build a layout registry.

    Each layout defines:
    - slot structure (image slots, text blocks, caption areas)
    - max content density
    - typography scale
    - spacing rules

    Slides choose layout by compatibility with slide_type + user config.

## 3) Creator configuration surface

### A. Presentation style presets

Model after creators:
- **Sierkovitz style** — data-heavy, tight claims, frequent charts, minimal flavor text
- **Rhystic Studies style** — narrative, visual motifs, pacing slides, quotes
- **Limited Level Ups style** — teaching-oriented, heuristics, gameplay scenarios, draft examples

Config example:

    {
      "style": "rhystic",
      "verbosity": "medium",
      "image_priority": "high",
      "data_density": "low"
    }

Claude prompt:

    Implement style presets that influence:
    - slide sequencing
    - slide types frequency
    - layout selection
    - text density
    - image usage
    - inclusion of quotes or data

    Make presets composable, not hard-coded.

### B. Narrative control

Let the creator define the *shape* of the talk.

Options:
- chronological
- thematic
- mechanics-first
- format-first
- card-first
- argument-driven

    {
      "narrative_mode": "chronological",
      "sections": [
        "definition",
        "early_history",
        "peak_power",
        "modern_usage",
        "conclusion"
      ]
    }

Claude prompt:

    Build a narrative planner.

    Input:
    - topic packet
    - narrative_mode
    - optional section overrides

    Output:
    - ordered slide plan with section boundaries

### C. Density controls

Controls:
- slides_per_minute
- max_cards_per_slide
- max_words_per_slide
- include_speaker_notes (true/false)
- include_citations (inline vs appendix)

Claude prompt:

    Add density controls that constrain:
    - number of slides
    - content per slide
    - grouping behavior (cluster vs individual card slides)

### D. Speaker notes generation

Each slide should optionally include:
- expanded explanation
- historical context
- citations
- jokes / tone (optional)
- transition cues

Claude prompt:

    Add speaker_notes generation.

    Notes must:
    - expand claims without duplicating slide text
    - include citations
    - flag uncertainty
    - optionally include rhetorical cues (pause, emphasis)

### E. Evidence transparency modes

Modes:
- **clean** (no citations visible)
- **annotated** (footnotes on slides)
- **research mode** (heavy provenance, confidence levels)

Claude prompt:

    Implement evidence modes.

    Each mode controls:
    - citation visibility
    - confidence indicators
    - inclusion of "uncertain" labels

### F. Image strategy

Controls:
- prioritize card images vs art crops
- allow duplicates across slides
- enforce unique cards per section
- zoom/crop preferences
- include artist credit

Claude prompt:

    Build an image selection strategy.

    Given candidate images:
    - rank by relevance
    - avoid redundancy
    - select variant based on slide_type

### G. Section-level customization

    {
      "sections": {
        "early_history": {
          "include": true,
          "max_slides": 5
        },
        "competitive_analysis": {
          "include": true,
          "data_density": "high"
        },
        "art_analysis": {
          "include": false
        }
      }
    }

Claude prompt:

    Add section-level overrides that modify:
    - slide count
    - slide types allowed
    - density
    - layout preferences

## 4) Advanced features

### A. "Argument graph" → slides
Instead of linear generation, build a graph of claims, supporting evidence, counterclaims. Then linearize into slides.

### B. Multi-output modes
Same topic → different outputs:
- lecture deck
- short-form YouTube deck
- Twitter thread outline
- article

Claude prompt:

    Allow output targets:
    - slideshow
    - short_video
    - article

    Each target uses the same topic packet but different constraints.

### C. Iterative refinement loop
After generation: mark slides as weak, regenerate only that section, swap layouts without regenerating content.

### D. Live presentation mode (later)
Presenter view with notes, timing cues, slide grouping, quick navigation by section.

## 5) What "good" looks like

A strong output deck should:
- feel like a **coherent argument**, not a list
- avoid repeating the same card without purpose
- show **why something mattered**, not just that it exists
- balance: cards, decks, formats, visuals
- allow the creator to talk naturally without reading slides

## 6) Synthesis prompt

    Refactor the slideshow generator into a presentation compiler.

    Add:
    - semantic slide types
    - layout registry
    - style presets (data-driven, narrative, teaching)
    - narrative planner
    - density controls
    - speaker notes
    - evidence modes
    - image strategy
    - section overrides

    Ensure:
    - full separation of content vs layout
    - deterministic output given same inputs + config
    - all uncertainty is preserved, not hidden

If implemented correctly, entering `"zombie archetypes in limited"` could produce a Sierkovitz-style data lecture, a Rhystic-style narrative essay, or a Limited Level Ups teaching breakdown — without rewriting the underlying research.
