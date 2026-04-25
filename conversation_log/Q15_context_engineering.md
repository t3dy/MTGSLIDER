# Q15 — Context engineering tips for all sources

## Verbatim user input

> give me tips for context engineering with all the sources I've names how can we create a coding environment and structured tables or databases or whatever that can be efficiently queried by LLMs and humans

## How I interpreted it

A meta question, not a build request. Wanted recommendations for organising the user's many data sources (Claudiens, EmeraldTablet, alchemy_scryfall, MTGSLIDER, SocialsDB, scattered .md notes) so that both LLMs and humans can query them efficiently.

Took the brief literally — *tips*, not implementation. Drew on what the user already does well (the `Claudiens/` provenance pattern, deterministic-before-LLM, idempotent scripts) and named the missing layer.

## What I built

[writing/CONTEXT_ENGINEERING.md](../writing/CONTEXT_ENGINEERING.md) — a recommendation document, ~1500 words:
- Inventory of the user's existing data sources with strengths/weaknesses for cross-querying
- Argument against a monolithic database (would strip provenance, would create migration chaos)
- Recommended pattern: **federated SQLite + shared `entities` contract** — each project keeps its rich schema; each adds a small uniform `entities` table that the federated reader joins
- Three patterns for LLM-queryability: SQLite FTS5, per-database `briefing.md`, JSON exports for context windows without file access
- Three patterns for human-queryability: CSV exports, static `index.html` per database, workspace-level `INDEX.md`
- Anti-patterns: don't unify schemas, don't standardise terminology across projects, don't embed-as-default (FTS5 first), don't migrate data away from project DBs
- A concrete small first step (pick TWO databases, demonstrate one cross-query) — explicitly NOT a build authorization

## What I deferred

The federated layer itself. Parked in `PARKING_LOT.md` as project-scale work.
