# Q11 — OED-style historical-trip skill

## Verbatim user input

> I'd like to make content that does historical trips like looks up a word like "conjure" or "sorcery" or "cantrip" in the OED to get a historical usage perspective and dating of first extant uses and changing definitions over time that work into our narratives in the slides. Give me a claude skill for doing this very generably and configurably by user input who could say order a dozen scripts focused on OED like historical trips for creature types connected with alchemy

## How I interpreted it

Two parts:
1. A Claude skill (real, invokable) that does etymology-style historical research on words
2. Configurable enough that a user can request a batch ("a dozen scripts focused on OED-style trips for creature types connected with alchemy")

The deliverable is a *meta-tool*. Recognised that subsequent queries (Q13, Q14) were variants of the same operation — same skill should handle all of them with a `source_type` parameter. Designed the skill around `etymology` / `biography` / `tradition` / `database_concept` source types so it covers words, persons, traditions, and concepts from the user's own databases.

Honest about the OED limitation: no public OED API, paywalled. The skill writes structured prompts the LLM fills from training data with explicit `confidence` and `source_attribution` fields rather than faking OED query results.

## What I built

`C:\Users\PC\.claude\skills\mtg-historical-trip\`:
- `SKILL.md` — full instructions with frontmatter (name + description), procedure, voice rules borrowed from `Claudiens/AFSTYLING.md`, batch mode, MTGSLIDER integration notes, output convention
- `templates/etymology.md` — first attestation, period definitions, semantic shift, MTG use, MTG connection, sources
- `templates/biography.md` — life dates, characteristic themes, canonical works, MTG resonances, synthesis
- `templates/tradition.md` — period, key texts, central concepts, MTG motifs
- `templates/database_concept.md` — for source items pulled from the user's own SQLite databases

Skill is registered and visible in the available-skills list as `mtg-historical-trip`.

## What I deferred

Actually generating any historical-trip cards — that's the user's call to invoke the skill on a specific batch. The 100-keyword list (`writing/100_magical_keywords.md`) is ready to be fed in.
