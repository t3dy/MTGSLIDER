# Q14 — Literary author tropes / alchemist tropes → MTG themes

## Verbatim user input

> or a topic could take the favorite tropes or haunts of a certain literary author and find mtg topics that illustrate those themes, in the same way we could use instead of a literary author a historical alchemist, magician, or [natural] philosopher

## How I interpreted it

Same meta-pattern again — another *source type* for the historical-trip skill. This is exactly what `source_type: biography` was designed for. The named figure (Borges, Paracelsus, John Dee, Ficino, Eliade, etc.) is the source; their characteristic themes are the bridges; MTG cards/themes that illustrate those themes are the output.

## What I built

The `biography.md` template is already in the skill (created in Q11 for exactly this case). Parked the *batch curation UI* — a way to maintain a reusable list of authors and re-run their trip cards as new MTG sets release — in `PARKING_LOT.md`. The batch UI is sprint-scale and not needed for the user to start using the skill; `mtg-historical-trip` can already process a list of names today.

## What I deferred

- Persistent author-list table in MTGSLIDER's SQLite schema (parked)
- Auto-rerun-on-new-set behaviour (parked)
