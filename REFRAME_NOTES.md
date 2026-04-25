# REFRAME_NOTES.md

## The reframe

The original Spec Dump 3 proposal called for a unified `Topic` table covering everything from "alchemists" to "tempo merfolk in Modern" to "black recursive one-drops". After analysis (`/plan-mercer-reframe`), this was found to be a category mistake bundling four genuinely different research objects under one schema.

## The four research-object types

| Type | Examples | Truth condition | Decay | Reusable? |
|---|---|---|---|---|
| **Theme** | alchemists, books, dreams, lab furniture, cards showing desks | Human judgment + art annotation | None — monotonic | **Yes — very** |
| **ArchetypeStudy** | tempo merfolk, zombie aristocrats | Tournament evidence | High | Partial |
| **FormatQuestion** | zombies in M14 limited, graveyard engines in Pioneer | Legality + dated decklists + B&R | None (already historical) | Yes |
| **SavedQuery** | black recursive one-drops | Scryfall query | None | It IS the query |

These types share an **interface** (review UI surface, packet export protocol, project membership, citations, provenance) but **not a schema, not evidence-scoring rules, and not a persistence model**.

## What slice 1 builds

Only **Theme** is implemented. It's the type where the "research once, reuse forever" promise is unambiguously true, and it exercises every part of the foundation (Scryfall, images, manual review, packet, .pptx) without dragging in format taxonomy, B&R timeline, or dated decklist parsing.

## What slice 1 does NOT build

- ArchetypeStudy (needs decklist parser + format taxonomy + B&R timeline as prerequisites)
- FormatQuestion (needs B&R timeline + format taxonomy + temporal legality as prerequisites)
- SavedQuery (probably not a stored object at all — at most a CLI shortcut later)
- The `topic_relationships` graph (premature without multiple instances)
- `topic_property_extraction` (the property bag is the schema admitting it doesn't know its shape; defer until we have actual properties to extract)
- `topic_comparison` (needs multiple themes ready for comparison; trivial CLI add later)

## Why two slideshow backends

Spec Dump 1 specified a template-driven slideshow (`v1_template`). Spec Dump 4 specified a presentation compiler (semantic slide types + layout registry + style presets) that supersedes it.

The compiler is the long-term right answer. The template is the thing that can ship today and prove the loop end-to-end. Building both:

- gives us a working .pptx output today (`v1_template`)
- proves the compiler architecture is real, not vaporware (`compiler` stub)
- lets each evolve independently against the same theme packet input
- makes it cheap to retire `v1_template` once `compiler` is mature

This is the only place in MTGSLIDER where two parallel implementations exist, and it exists because the two specs reflect a genuine product question (deterministic template vs. configurable compiler) where the answer depends on usage we haven't seen yet.
