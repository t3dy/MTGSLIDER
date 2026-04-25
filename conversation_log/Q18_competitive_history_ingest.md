# Q18 — Ingest the entire competitive history of Magic

## Verbatim user input

> can we just ingest the history of competitive magic and build our own database of knowledge of cards that have had tournament success in all the formats and other notable information that will inform our historical haunts into the content and its connections with historical magic and the history of english usage of the terms

## How I interpreted it

A genuine ask, but project-scale in a way the user may not have fully sized. The competitive history of Magic spans 1993–present, 12+ named constructed formats, thousands of premier-level events, hundreds of thousands of decklists. Useful sources: MTGTop8 (HTML scrape, respect ToS), MTG Wiki archetype pages, Wizards' own decklist coverage articles, MTGGoldfish, Channel Fireball.

The Deckard plan I just wrote ([DECKARD_BOUNDARY_PLAN.md](../writing/DECKARD_BOUNDARY_PLAN.md)) already covers the architecture for this exact undertaking — D3 (deterministic decklist parsing), D5 (tournament-result provenance), D6 (deck-membership SQL queries), V4 (scrape-vs-cite boundary on each source).

So "can we" — yes, the architecture is laid out. "Let's just do it" — no, this is multi-week to multi-month work and should be sliced via `/plan-runciter-slice`. A reasonable first slice would be: ONE format (probably Modern, since it has the cleanest archive), ONE year (most recent full season), ONE source (MTGTop8), ~50 decks. Prove the loop end-to-end, then expand by format and back through time.

## What I built

- New parking entry in [PARKING_LOT.md](../PARKING_LOT.md): "Competitive Magic history ingest"
- The Deckard plan already provides the architectural ground; no new design needed
- Recommended a Modern-2025 first slice (project-scale; gated on `/plan-runciter-slice`)

## What I deferred

The ingest itself — parked at project scale, with the explicit warning that "let's just ingest everything" is the spec-creep pattern from earlier in this session. Recommended slice 1 = one format, one year, one source.
