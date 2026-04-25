# Q20 — Deckard plan for ChatGPT-chat ingest

## Verbatim user input

> I'd also like a Deckard plan like the one above for digging into my ChatGPT chats where I discuss mtg projects and create databases of my prompts and outputs and designs and desires to add to a section of our database or memory or system files

## How I interpreted it

Same flavor as Q17 — a Deckard boundary plan, this time for an MTGSLIDER-adjacent project that ingests the user's ChatGPT chat history (where MTG-related prompts, outputs, design ideas, and "desires" live), structures them, and feeds them into either MTGSLIDER's database, the workspace memory layer, or system documentation.

This is closely related to Q12 (tweet-archive mining) — both are *personal-archive ingestion* tasks. Likely the same data home is `C:\Dev\SocialsDB` or a sibling. Per the SocialsDB CLAUDE.md, that project already aspires to integrate "GPT Archive" — but no DB file is currently present.

## What I built

- [writing/DECKARD_BOUNDARY_PLAN_chatgpt_ingest.md](../writing/DECKARD_BOUNDARY_PLAN_chatgpt_ingest.md) — second Deckard plan, parallel structure to the first
- New parking entry in [PARKING_LOT.md](../PARKING_LOT.md): "ChatGPT chat ingest for MTG project archaeology"

## What I deferred

The actual ingest. The chat archive may exist locally as a ZIP from OpenAI's data export. Locating it and confirming format is the prerequisite for slice 1.
