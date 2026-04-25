# OVERLAY_INTEGRATION.md

How MTGSLIDER's database plugs into the existing `MTGDraftOverlay` project to deliver live, transparent, toggleable in-game overlays carrying historical / cultural / linguistic commentary alongside (or instead of) the existing strategic-advice content.

## What already exists in MTGDraftOverlay

Per `C:\Dev\mtg-overlay-plan.md`:
- **Platform:** Windows-only, runs on the same machine as MTG Arena
- **Card detection:** Player.log scrape → grpId → oracle_id (already wired)
- **Draft-pick UI:** compact badges per pack slot + side panel keyed by slot position
- **Side-panel pattern:** "always visible when draft is active" — *this is the integration point we extend*
- **Hide / show:** foreground detection (auto-hide when MTGA loses focus); hotkeys for visibility
- **Multi-monitor:** overlay follows MTGA window
- **Stack:** Node.js, vitest

The overlay already has the hard parts solved: knowing which card is on screen and rendering a non-intrusive panel adjacent to MTGA. **What's missing for the user's ask is a content layer — the panel currently shows pick ratings; we add commentary content alongside or in tabs.**

## The integration point

Two new things:

1. **MTGSLIDER must expose a read API.** Not a web service — a small local Node-readable interface. Two options, both small:
   - **Option A (preferred):** A SQLite read-only handle on `MTGSLIDER/data/mtgslider.sqlite` from the Node overlay process. Node has good SQLite bindings (`better-sqlite3`). The overlay queries the same file MTGSLIDER's Python writes; no IPC, no HTTP, no service to manage.
   - **Option B:** A tiny Python HTTP server (`uvicorn`/`flask` on `localhost:7843`) that the overlay calls. More complex to operate; adds a process the user has to remember to start. Use only if Node-side SQLite proves problematic.

2. **A panel content schema** the overlay can render generically, regardless of which content type is being shown. Each panel "card" looks like:
   ```ts
   interface CommentaryPanel {
     oracle_id: string
     card_name: string
     panel_type: 'strategic' | 'historical' | 'linguistic' | 'lore'
     title: string                 // e.g. "Etymology of 'conjure'"
     summary: string               // 1–2 sentences, headline
     body_markdown: string         // rich content, scrollable
     citations: { label: string, url?: string }[]
     confidence: 'high' | 'medium' | 'low'
     review_status: 'reviewed' | 'unreviewed'    // overlay HIDES unreviewed by default
     mtgslider_source: string      // e.g. "theme:books-in-magic", "etymology:conjure"
   }
   ```

The overlay shows tabs (strategic / historical / linguistic / lore) keyed by `panel_type`. Tabs with no content for the current card simply don't appear. Tabs with `review_status='unreviewed'` content show a small "draft" badge.

## Data flow at runtime

```
MTG Arena draws a card on screen
        ↓
MTGDraftOverlay's existing log scraper resolves oracle_id
        ↓
Overlay queries MTGSLIDER read API:
    SELECT * FROM v_card_commentary WHERE oracle_id = ?
        ↓
MTGSLIDER returns 0..N CommentaryPanel rows (all four types may apply)
        ↓
Overlay renders tabs in its existing side-panel slot
        ↓
User toggles visibility / switches tabs / dismisses with hotkey
```

The view `v_card_commentary` is the contract. It joins:
- `theme_card_links` → which themes does this card belong to (approved only)
- `theme.packet` → the theme's curated note
- `historical_trips` (proposed table) → etymology / biography / tradition cards that reference this card
- `forum_summaries` (proposed table, parked) → fan takes if any
- `competitive_appearances` (proposed table from Q18 plan) → famous decks the card was in

Each row carries `review_status` and `confidence`. The overlay defaults to showing only `reviewed`. A "preview mode" toggle in the tray icon lets the user see drafts.

## What's new vs reused

| Need | Reused from existing overlay | New build |
|---|---|---|
| Detecting card on screen | yes — log scraper exists | nothing |
| Rendering side panel | yes — side-panel UI exists | adapt to render `CommentaryPanel` |
| Toggle / hotkeys | yes — already designed | add hotkey for tab switching |
| Foreground / multi-monitor | yes | nothing |
| Card → oracle_id resolution | yes | nothing |
| **Content** | the existing 17Lands draft ratings | **MTGSLIDER read API + the four panel_type content layers** |

## Constructed-play mode (the user's broader ask)

The existing overlay is draft-only. Extending to constructed live play needs:
- **Card-on-screen detection during a constructed game.** MTG Arena's Player.log emits events for every revealed card (your hand, spells cast, opponent reveals, exiled cards, etc.). The plumbing is the same as draft; the *triggering events* are different. This is overlay-side work, not MTGSLIDER work.
- **Less aggressive panel display.** Drafts have natural pause-points (between picks); constructed play does not. The overlay needs a "passive mode" — content available on hover or hotkey, never auto-popping. This is overlay UX.

Both are MTGDraftOverlay-side; MTGSLIDER's read API is identical regardless of game mode.

## Boundaries (Deckard discipline)

Reusing the framework from [DECKARD_BOUNDARY_PLAN.md](DECKARD_BOUNDARY_PLAN.md):

- **Deterministic:** card-on-screen detection, oracle_id lookup, SQL query against `v_card_commentary`, panel rendering. No LLM in the live path.
- **Probabilistic, but pre-computed:** the *content* of the commentary panels — historical-trip cards, scholarly notes, theme assignments — is LLM-assisted at *authoring time* (per the existing Deckard plan), reviewed by the user, then stored as `reviewed` content in MTGSLIDER's DB. **At gameplay time the LLM is not invoked.** This is the right boundary: live overlay must be fast and deterministic; quality comes from the offline curation.
- **Forbidden:** invoking an LLM during gameplay to generate commentary on demand. Latency, cost, and reliability all argue against it. If a card has no curated content, the panel shows a "no commentary yet" placeholder with a button to "stage this card for commentary" — which queues a background `mtg-historical-trip` invocation between sessions.

## Prerequisites

Before the integration is buildable:
1. MTGSLIDER's schema needs an `oracle_id` indexed on `cards` (already there as `cards.oracle_id` — confirmed in `schema.sql`).
2. MTGSLIDER's schema needs the `historical_trips` table (proposed; not yet built — would store the structured output of the `mtg-historical-trip` skill).
3. The `v_card_commentary` view needs to be designed (small SQL, can be written when the integration starts).
4. Decision: SQLite handle from Node (Option A) vs HTTP service (Option B). Recommend A.
5. The overlay project needs a small content-panel mode added alongside its existing rating-panel mode.

None of these are large. The largest is the *content* itself — having enough curated commentary to make the overlay feel populated. That's the existing MTGSLIDER pipeline running over time, not a new build.

## Out of scope (parked)

- Real-time LLM invocation during gameplay (forbidden per Deckard)
- TTS / audio commentary during play (not asked for; would be a separate project)
- Mobile / Arena Mobile support (overlay is Windows desktop)
- MTGO support (different log format, different work)
- Multiplayer / streaming overlay (different audience, different constraints)

## Recommended slice 1 (when the user is ready to build)

Smallest end-to-end integration:
1. Add `historical_trips` table to MTGSLIDER schema
2. Generate one historical-trip card for ~5 well-known cards (e.g. *Counterspell*, *Lightning Bolt*, *Wrath of God*, *Llanowar Elves*, *Sol Ring*) using the `mtg-historical-trip` skill
3. Build `v_card_commentary` view returning historical content for those 5 cards
4. Add a single new "Historical" tab to MTGDraftOverlay's existing side panel, reading from the SQLite handle
5. Demo: open a draft, get a pick that includes one of the 5 cards, see the historical tab populate

If that loop works end-to-end on draft for 5 cards, expanding to constructed mode and to the full content corpus is engineering, not architecture.
