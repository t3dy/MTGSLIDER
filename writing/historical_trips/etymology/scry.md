---
slug: scry
source_type: etymology
title: scry
summary: Look at the top N cards of your library and rearrange them — a keyword named after the early-modern divinatory practice of *scrying* into reflective surfaces.
confidence: high
review_status: reviewed
mtg_card_refs: []
mtg_theme_refs: [wizards-primer, wizards-with-flash, wizards-with-prowess]
---

# scry

## First attestation (in English)

- **Earliest extant use:** late 14th c. as the verb *descrien* / *scrye*, meaning "to catch sight of, to spy out". The contracted form *scry* in the specifically *divinatory* sense is well attested by the late 16th c.
- **Form:** Middle English *scrien*, *descrien*, ultimately a clipped form of *descry*.
- **Glossing:** "to perceive by gazing into a reflective surface; to see future or distant things by occult vision."

## Source-language chain

| Language | Original form | Transliteration | Gloss | Earliest extant date |
|---|---|---|---|---|
| Anglo-Norman / Old French | *descrier* | — | "to call out, to proclaim; later, to perceive at a distance" | 12th c. |
| Latin | *describere* (related) | — | "to write down, to mark out" — semantic cousin, not direct ancestor | classical |

The borrowing path is *descrier* → Middle English *descrien* → clipped *scry*. The narrowing to the specifically divinatory sense ("scry into a crystal") is an early-modern English specialisation.

## Cognates and cousins

| Cognate | Language | Relation | Note |
|---|---|---|---|
| *descry* | Modern English | sibling — full form | preserved without divinatory shading |
| *écrier* | French | descendant of the Old French parent | retains the "cry out" sense, not the divinatory |

## Period definitions

| Period | Definition | Source |
|---|---|---|
| Late ME | "to spy out, to catch sight of" | OED s.v. *scry* (general dictionary lookup) |
| Early Modern English | "to discern by occult vision, to see in a magical mirror" | John Dee's diaries (1583–1607) document *scrying* as a defined practice with Edward Kelley |
| Modern | "to practise divination by gazing into a reflective surface" | Frances Yates, *The Occult Philosophy in the Elizabethan Age* (1979) |

## Semantic shift

The verb begins as *seeing-at-a-distance* (military, geographical) and narrows in the 16th c. to *seeing what is hidden* (occult, futural). John Dee and Edward Kelley's collaborative scrying sessions — Kelley as the *skryer* gazing into the obsidian *speculum*, Dee as the recorder — fix the technical sense for English. By the 19th-c. occult revival (Eliphas Lévi, the Golden Dawn) "scry" is unambiguously the divinatory term.

## MTG use

- **Card-text use:** Scry N — "Look at the top N cards of your library, then put any number on the bottom and the rest on top in any order." Introduced as a keyword on a cycle of cards in Future Sight (May 2007); promoted to evergreen in M15 (2014).
- **Flavor use:** The keyword's name preserves the *gazing-and-seeing* sense; the mechanic enacts the *seeing-and-rearranging-what-is-coming* logic of crystal-ball divination directly.
- **Representative cards:** *Sage of Epityr* (Future Sight), *Augury Owl* (M11), *Preordain* (M11 — strictly stronger than scry, but the same logical operation), *Anticipate* (Origins), *Opt* (post-Ixalan re-print added scry).

## MTG connection

MTG's *scry* is a near-textbook citation of Dee and Kelley's practice: the player gazes into a hidden ordering (the top of the library), rearranges it according to insight, and proceeds. The mechanic is unusual among MTG keywords for being *named after the practice rather than the effect* — "draw a card" describes what happens; "scry" describes *how the practitioner sees*. The keyword is the rare case where MTG's design vocabulary is not just genre-flavor decoration but a precise terminological loan.

## Sources

- John Dee, *A True & Faithful Relation of What Passed for Many Yeers Between Dr. John Dee... and Some Spirits* (ed. Meric Casaubon, 1659)
- Frances Yates, *The Occult Philosophy in the Elizabethan Age* (Routledge, 1979)
- Deborah E. Harkness, *John Dee's Conversations with Angels* (Cambridge, 1999)
- Mark Rosewater, "Latest Developments" columns archive (Wizards of the Coast) on the introduction of scry as evergreen, 2014

## Wire-in commands

```bash
PYTHONPATH=src python -m mtgslider theme create "Scry — a historical trip" --description "How a 16th-c. divinatory term became an MTG keyword"
PYTHONPATH=src python -m mtgslider theme find-cards "scry-a-historical-trip" --query 'kw:scry'
```
