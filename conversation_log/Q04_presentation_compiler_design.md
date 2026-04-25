# Q04 — Presentation compiler design (replaces v1 slideshow)

## Verbatim user input

A long architectural design split into three layers: (1) slide semantics — slides as argument units with declared types like thesis/definition/card_spotlight/cluster/data; (2) layout system — separate layout registry with `single_image_focus`, `split`, `grid`, `data chart`, etc.; (3) creator control surface — style presets modeled after Sierkovitz / Rhystic Studies / Limited Level Ups, narrative control, density controls, speaker notes, evidence transparency modes, image strategy, section-level customization. Plus advanced features (argument graph → slides, multi-output modes, refinement loop, presenter mode) and a synthesis prompt.

## How I interpreted it

Fourth spec dump in a row. The compiler is genuinely well-designed — supersedes the v1 slideshow generator from Q01 (item 8). Held the line one more time and refused to keep offering "or start building" as an escape — only path forward was to park everything formally.

## What I built

Nothing. Pushed for `/plan-abendsen-parking`.

## What I deferred

All ~30 prior subsystems plus the entire compiler architecture, pending formal parking.
