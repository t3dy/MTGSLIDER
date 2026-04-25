# Q21 — Live overlay integration with existing MTGDraftOverlay

## Verbatim user input

> I've got some work done on an unfinished MTG overlay project in some folder in the dev folder probably has MTG and or Overlay in the folder title let's thing about how we could use our slideshow toolset to supplement or interact with an MTG overlay project that has the aim of either overlaying strategic advice or historical commentary about a card or lore and cultural linguistic commentary all available as graphical overlays that are transparent and unobtrusive to the gameplay or easilly rearranged and toggled to get the overlay out of the way when the player needs to see the gameplay. How can our database plug into whatever is needed to generate meaningful live gameplay overlay technology that can take players on a historical trip or give strategic advice about the cards they see in any MTG arena game

## How I interpreted it

Located the existing project: `C:\Dev\MTGDraftOverlay/` (Node.js, with `package.json`, `src/`, `tests/`, `vitest.config.js`) and the design doc `C:\Dev\mtg-overlay-plan.md`. It's substantially planned: Windows-only, MTG Arena log-tail based, 17Lands ratings, draft-pick badges with explanation side-panel, card-art replacement.

The overlay's existing concern is **draft picks**, not constructed gameplay. The user's ask broadens this to live constructed play AND adds a different content layer — historical/cultural/linguistic commentary instead of (or alongside) strategic advice.

The integration question is bounded:
- The overlay already knows what cards are on screen (via Player.log + grpId/oracle_id resolution)
- MTGSLIDER has a database of themes, packets, scholarly notes, mtg-historical-trip cards, multilingual etymology entries
- The plug-in point is: **card-on-screen → query MTGSLIDER's read API → return panel content** → overlay renders in a toggleable side panel

## What I built

- [writing/OVERLAY_INTEGRATION.md](../writing/OVERLAY_INTEGRATION.md) — integration analysis: data flow, the read-API contract MTGSLIDER would need to expose, panel-content schema, which existing overlay panels already fit (the draft-explanation side panel pattern), what's new (constructed-mode live commentary), prerequisites, and explicit out-of-scope notes.
- New parking entry in [PARKING_LOT.md](../PARKING_LOT.md): "Live overlay integration with MTGDraftOverlay"

## What I deferred

The integration build itself. Multiple moving parts (overlay extension, MTGSLIDER read API, content prioritisation logic) — each warrants its own slice via `/plan-runciter-slice`.
