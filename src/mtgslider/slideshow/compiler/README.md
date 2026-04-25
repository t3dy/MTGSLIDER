# compiler — presentation compiler

Spec Dump 4 architecture. Status: **functional with three differentiated presets.**

## What's wired today

- **Semantic slide types** ([slide_types.py](slide_types.py)): each slide is an `ArgumentUnit` declaring `slide_type`, `rhetorical_role`, required/optional content fields, evidence references, and speaker notes. Validation rejects malformed units. Types: `thesis`, `definition`, `card_spotlight`, `cluster`, `visual_motif`, `data`, `key_takeaways`, `transition`, `conclusion`, `citations`.
- **Layout registry** ([layouts.py](layouts.py)): each layout declares slot structure and slide-type compatibility. Layouts: `single_image_focus`, `split_image_text`, `grid_2x2`, `cluster_grid_dense` (3x3), `data_chart_text`, `takeaways`, `text_only`.
- **Style presets** ([presets.py](presets.py)): `rhystic`, `sierkovitz`, `teaching`. Each is a config dict that produces a measurably different deck — see `tests/test_compiler_differentiation.py` for the regression locks.
- **Narrative planner** ([planner.py](planner.py)): three preset-specific planners produce different slide sequences from the same packet:
  - rhystic → narrative arc with visual motif and 6+ image-rich spotlights
  - sierkovitz → data slide first, 3 spotlights, then dense cluster grid
  - teaching → definition + "what to look for" + spotlights + key takeaways
- **Aggregate stats** ([stats.py](stats.py)): color, type, and mana-value distributions over a curated set. Used by the data slide.
- **Speaker notes** ([notes.py](notes.py)): three voices (`rich` / `terse` / `heuristic`), one per preset. Notes are deterministic restatements of packet facts in a voice matching the creator profile — never LLM-generated.
- **Evidence transparency** (in [renderer.py](renderer.py)): `clean` mode (rhystic) shows no on-slide citations; `annotated` mode (sierkovitz, teaching) adds a "via Scryfall · {id} · {variant}" footer to evidence-bearing slides.
- **Validation gate** ([generator.py](generator.py)): if the planner emits malformed argument units, the generator refuses to render rather than silently producing broken slides.

## What's NOT wired (deferred)

- Density controls beyond `max_words_per_slide` and the `density` selector ("low/medium/high")
- Section-level overrides (`{"sections": {"early_history": {...}}}`)
- Argument-graph linearization — planner is still linear
- Multi-output modes (only `.pptx`, no article/short-video)
- Iterative refinement loop ("regenerate this section, swap that layout")
- Live presenter mode
- Image strategy: variant selection per slide_type, dedup-across-section enforcement
- Inline citations (numbered footnotes); only the simple "via Scryfall" footer is wired

## Why a compiler not a template

The presets earn their separation: see `tests/test_compiler_differentiation.py` — three preset fingerprints, three voices for speaker notes, and v1 is structurally distinct from every compiler output. If those tests pass and any two preset outputs become structurally identical, that's a regression.
