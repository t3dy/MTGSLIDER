---
slug: sorcery
source_type: etymology
title: sorcery
summary: A spell that resolves only at sorcery speed — named after the medieval legal-pejorative term for divinatory and harmful magic, *sortilegium*, "drawing of lots."
confidence: high
review_status: reviewed
mtg_card_refs: []
mtg_theme_refs: [wizards-primer, lab-and-alchemy]
---

# sorcery

## First attestation (in English)

- **Earliest extant use:** c. 1300 in Middle English as *sorcerie*, "the practice of magic, witchcraft."
- **Form:** Middle English *sorcerie*, from Old French.
- **Glossing:** "the use of supernatural arts for harmful or divinatory ends."

## Source-language chain

| Language | Original form | Transliteration | Gloss | Earliest extant date |
|---|---|---|---|---|
| Old French | *sorcerie* | — | "magic, witchcraft" | 12th c. |
| Vulgar Latin | *sortiārius* (reconstructed) | — | "one who casts lots" | post-classical |
| Latin | *sors, sortis* + *legere* | — | "lot, fate" + "to choose, to read"; *sortilegium* = "the drawing of lots for divination" | classical |

The root sense is *divination by drawing lots* — *sortes Vergilianae*, the practice of opening Virgil at random and reading the line as oracle, is the classical exemplar. Medieval Christian Latin demotes the practice as illicit; *sortilegium* in canon law is a prosecutable form of magic (see the *Decretum Gratiani*, c. 1140). The Old French *sorcerie* inherits the pejorative weight, and Middle English inherits it intact.

## Cognates and cousins

| Cognate | Language | Relation | Note |
|---|---|---|---|
| *sorcerer* | English | agent noun | the practitioner |
| *sortilege* | English / French | direct nominalisation | preserved in legal-historical contexts |
| *sors* | Latin | root | "lot, oracle, share, fate" |
| *Hexerei* | German | parallel formation | independent root, same semantic field |

## Period definitions

| Period | Definition | Source |
|---|---|---|
| Late ME | "the use of magic, especially harmful magic; witchcraft" | OED s.v. *sorcery* |
| Early Modern | a *legal* category — sorcery as prosecutable offense, distinct from *natural magic* and *theurgy* | the Malleus Maleficarum (1486); Reginald Scot, *The Discoverie of Witchcraft* (1584) |
| Modern | "magic, esp. of a folkloric or fantastical kind" | weakened, genre-fictional |

## Semantic shift

The historical arc is *divination-by-lot* → *illicit divination* → *illicit magic generally* → *fictional magic*. The narrowing happens through legal practice: the *sortilegium* of casting lots becomes the prototype of all illicit magic in canon law, and the term broadens to cover anything in that legal category. The modern weakening to genre-fiction usage is post-Tolkien; in MTG, the term is purely architectural rather than legal-pejorative.

## MTG use

- **Card-text use:** *Sorcery* is one of the original card types in Alpha (1993), denoting a spell that may only be cast at *sorcery speed* — during the controller's main phase, with an empty stack. The contrast is *instant*. Mechanically: sorceries are slower, often more powerful per mana than instants.
- **Flavor use:** The sorcery card type carries the heaviest, most "ritual" framing of any spell type. *Wrath of God*, *Damnation*, *Cruel Ultimatum*, *Time Spiral* — sorceries are the cards that *take time* and *reorder the world*.
- **Representative cards:** *Wrath of God* (Alpha), *Time Walk* (Alpha — Power Nine), *Cruel Ultimatum* (Shards of Alara), *Time Spiral* (Time Spiral block).

## MTG connection

MTG's *sorcery* preserves the historical sense of *the slower, more deliberate, more ritualised form of magic*. The mechanical restriction (sorcery-speed only) and the flavor association (mass effects, world-altering changes, ritual destructions) both descend from the medieval legal sense of *sortilegium* as the *deliberate* practice — distinguished from instant reactions, which in MTG are *instants* and in medieval theology are closer to *theurgy* or *natural philosophy*. The card type is one of MTG's oldest and most stable; the etymology was almost certainly not on Richard Garfield's mind in 1993, but the lexical fit is exact.

## Sources

- *Decretum Gratiani* (c. 1140), Causa 26
- Heinrich Kramer, *Malleus Maleficarum* (1486)
- Reginald Scot, *The Discoverie of Witchcraft* (1584)
- OED s.v. *sorcery*
- Frances Yates, *Giordano Bruno and the Hermetic Tradition* (Routledge, 1964) on the early-modern legal taxonomy of magic

## Wire-in commands

```bash
PYTHONPATH=src python -m mtgslider theme create "Sorcery — a historical trip"
PYTHONPATH=src python -m mtgslider theme find-cards "sorcery-a-historical-trip" --query 't:sorcery cmc<=3 -is:reprint'
```
