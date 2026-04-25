# Q19 — Multilingual etymology + relational browsing UI

## Verbatim user input

> I'd like to pay attention to the other languages where all our magical terminology comes from and we can do a section of the website where you can do relational browsing of the words with linguistic and cultural commentaries

## How I interpreted it

Two parts:
1. Multilingual sourcing — magical terminology in MTG (and in scholarship) descends from Greek (*pharmakon*, *magos*, *hermeticus*), Latin (*sortilegium*, *coniuratio*), Arabic (*al-kīmiyāʾ* → alchemy, *al-iksīr* → elixir, *talsam* → talisman), Hebrew (*qabbalah*, *golem*), Old Norse (*galdr*, *seiðr*), Middle English, French (*sorcerie*), German (*hexen*), and others. The etymology cards already produced by `mtg-historical-trip` should capture these chains, not just the English line.
2. A *relational browsing* website section — given a term, navigate to its source-language root, then to other terms sharing that root, with linguistic + cultural commentary.

Part 1 is small: extend the etymology template to require source-language fields. Doing it now.
Part 2 is project-scale: a graph UI over a `term_relationships` table. Parking it.

## What I built

- Extended [`mtg-historical-trip/templates/etymology.md`](file://C:/Users/PC/.claude/skills/mtg-historical-trip/templates/etymology.md) with a **Source-language chain** section (Greek/Latin/Arabic/Hebrew/Old Norse/Middle English/French/German lines, each with original script, transliteration, gloss, and earliest extant date) and a **Cognates and cousins** section (terms sharing the same root, in any language, with one-sentence relationship notes).
- New parking entry in [PARKING_LOT.md](../PARKING_LOT.md): "Multilingual term-relationships browsing UI" — a website section over `term_relationships`, with linguistic + cultural commentary, project-scale.

## What I deferred

The browsing UI itself. Parked. The data layer (multilingual fields in etymology cards) is in place now, so when the UI is built it has something to render.
