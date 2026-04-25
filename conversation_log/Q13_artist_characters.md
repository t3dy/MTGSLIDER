# Q13 — Artist character types from claudiens / alchemydb / hermeticdb

## Verbatim user input

> a topic could be artist character types that could illustrate historical connections between alchemists and artisanal culture which should be discussed in my databases claudiens, alchemydb, and the hermeticdb

## How I interpreted it

Two reads:
1. Suggesting another *kind* of source for the historical-trip skill — artist character types crossed with the user's scholarly databases
2. Pointing at three databases by name: `claudiens`, `alchemydb`, `hermeticdb`

Located: `C:\Dev\Claudiens\db\atalanta.db` (the Atalanta Fugiens scholarship DB) and `C:\Dev\EmeraldTablet\db\emerald_tablet.db`. There's also `C:\Dev\alchemy_scryfall/` and `C:\Dev\renaissance magic/`.

This ask is the same meta-pattern as Q11 — needs `source_type: database_concept` in the historical-trip skill. The skill already supports it. The *missing* piece is the federated query layer that lets the skill actually read across those databases.

## What I built

- `database_concept.md` template in the skill (covers the per-source schema for this case)
- Parked the federated query layer as its own item in `PARKING_LOT.md` — it's project-scale work
- `writing/CONTEXT_ENGINEERING.md` ([link](../writing/CONTEXT_ENGINEERING.md)) describes the proposed federated approach concretely (shared `entities` contract per database, FTS5 over summaries, briefing.md per project)

## What I deferred

The federated layer itself. The skill is ready to consume per-database concepts once they're indexed, but indexing the user's existing scholarly DBs is a multi-week undertaking and is parked.
