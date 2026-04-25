---
slug: conjure
source_type: etymology
title: conjure
summary: Bring something into being by speech — the verb that named medieval and early-modern ritual evocation, now applied to MTG's Alchemy mechanic for creating cards inside the game.
confidence: high
review_status: reviewed
mtg_card_refs: []
mtg_theme_refs: [wizards-primer, lab-and-alchemy]
---

# conjure

## First attestation (in English)

- **Earliest extant use:** c. 1290 in Middle English as *cunjuren*, "to call upon (a deity, a demon) by oath; to invoke."
- **Form:** Middle English *conjuren*, from Old French *conjurer*.
- **Glossing:** "to swear together, to bind by oath; (transferred) to summon a spirit by adjuration."

## Source-language chain

| Language | Original form | Transliteration | Gloss | Earliest extant date |
|---|---|---|---|---|
| Old French | *conjurer* | — | "to plot together; to invoke by oath" | 12th c. |
| Latin | *coniurāre* | — | *con-* (together) + *iurāre* (to swear); "to swear together, to conspire" | classical |

The crucial semantic step happens in Latin: *coniurāre* in classical use was *secular* (legal-political — to bind a confederation by oath), but in late-antique and medieval Christian Latin it acquires the *spiritual* sense of binding a spirit by sacred oath. The English verb inherits both: *conjuration* in the legal sense (rare, archaic) and the magical sense (canonical).

## Cognates and cousins

| Cognate | Language | Relation | Note |
|---|---|---|---|
| *conjuration* | English | nominal sibling | the act |
| *conjuror* | English | agent noun | the practitioner |
| *coniuratio* | Latin | direct ancestor | secular *and* sacred sense |
| *conjuré* | French | passive | "sworn", in legal/political sense |
| *Beschwörung* | German | structural cognate | "swearing-upon", same metaphor |

## Period definitions

| Period | Definition | Source |
|---|---|---|
| Middle English | "to invoke or summon by oath, especially a spirit" | OED s.v. *conjure* |
| Early Modern | "to perform magical operations involving the calling of spirits" | the *Picatrix* tradition; Cornelius Agrippa, *De Occulta Philosophia* (1531) |
| Modern colloquial | "to bring forth as if by magic; to call to mind" | weakened, metaphorical |

## Semantic shift

The shift is from *binding by oath* → *binding a spirit by oath* → *summoning a spirit* → *making something appear*. The medieval grimoire tradition (the *Picatrix*, the *Sworn Book of Honorius*, the *Lemegeton*) operationalises the verb: a *conjuration* is a specific spoken formula that compels a named spirit to appear. The colloquial sense ("to conjure up a memory") is a modern weakening of that operational sense.

## MTG use

- **Card-text use:** *Conjure* is a keyword action in MTG Arena's Alchemy format (introduced 2021), distinct from *create* and *make*. Specifically: "to conjure a card" means to put a card that did not exist in any zone before into a zone — typically a player's hand or library. It is a digital-only mechanic, unsupported in paper Magic.
- **Flavor use:** The choice of "conjure" rather than "summon" or "create" is deliberate. *Summon* was used in Alpha for casting creatures and was retired (because it implied removal-from-elsewhere). *Create* is reserved for tokens. *Conjure* fills a third semantic slot: bringing a *named, specific card* into being from nothing.
- **Representative cards:** *Hidetsugu's Two-Step* (Alchemy version), *Conjurer's Mantle*, *Erithizon Snitch* — though the cleanest examples are Alchemy-only and not on paper.

## MTG connection

MTG's *conjure* is the rare keyword that names *what the practitioner does* rather than *what happens to the world*. To conjure a card is to perform the verb in the medieval sense: to call something into being by naming it. The choice of this term rather than the available alternatives reads, in the design context, as a deliberate citation of the conjuror tradition — the figure who *speaks* what then *appears*. Mark Rosewater's design columns have not (to my knowledge as of 2026) discussed the etymological choice explicitly, but the lexical fit is too precise to be accidental.

## Sources

- Cornelius Agrippa, *De Occulta Philosophia Libri Tres* (1531)
- *Picatrix: The Latin Version of the Ghāyat al-Hakīm* (ed. David Pingree, Warburg Institute, 1986)
- OED s.v. *conjure, v.*
- Wizards of the Coast, MTG Arena Alchemy mechanics announcement (December 2021)

## Wire-in commands

```bash
PYTHONPATH=src python -m mtgslider theme create "Conjure — a historical trip"
PYTHONPATH=src python -m mtgslider theme find-cards "conjure-a-historical-trip" --query 'o:conjure'
```
