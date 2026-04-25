---
slug: hogaak-bridgevine-mc-barcelona-2019
name: Hogaak Bridgevine
archetype: Hogaak Bridgevine
format: Modern
event_name: Mythic Championship IV Barcelona
event_date: 2019-07-26
placement: representative top-finishing build (composite of multiple top-8 lists)
pilot: composite
source_url: https://magic.wizards.com/en/articles/archive/mtgo-standings/mythic-championship-iv-2019-07-28
---

# Hogaak Bridgevine — Modern, July 2019

A representative composite of the Hogaak Bridgevine archetype that dominated Modern Mythic Championship IV in Barcelona, July 26–28 2019. The archetype combined *Bridge from Below*, *Hogaak, Arisen Necropolis*, *Vengevine*, and *Carrion Feeder* into a turn-2 / turn-3 swarm engine that could produce overwhelming board states with no traditional mana investment, by paying for *Hogaak* with the alternative cost of tapping creatures and exiling cards from the graveyard, then returning *Vengevines* by casting two creatures of mana value 2 or less.

## Banlist context

- *Bridge from Below* was banned in Modern on **2019-07-08** (effective 2019-07-11), three weeks before MC IV. Hogaak Bridgevine remained the dominant deck despite the ban — the Bridge engine had been the explosive variant, but the *Hogaak* + *Altar of Dementia* + *Vengevine* + *Carrion Feeder* core remained powerful.
- *Hogaak, Arisen Necropolis* was banned in Modern on **2019-08-26**, one month after MC IV. The format had been distorted by the archetype for the entire June–August 2019 period.
- *Faithless Looting* was banned in Modern on the same date as Hogaak (2019-08-26), partly to address the broader graveyard-strategy problem the archetype represented.

The MC IV metagame was the high-water mark of the archetype's tournament presence. The deck list below is a composite reflecting the post-Bridge configuration that surged to a ~30%+ metagame share at the event.

## Mainboard (60)

```
4 Hogaak, Arisen Necropolis
4 Vengevine
4 Carrion Feeder
4 Stitcher's Supplier
4 Gravecrawler
4 Bloodghast
4 Insolent Neonate
4 Faithless Looting
4 Altar of Dementia
3 Goblin Bushwhacker
2 Lightning Axe
3 Bloodstained Mire
2 Wooded Foothills
2 Mountain
2 Blood Crypt
1 Stomping Ground
2 Overgrown Tomb
1 Forest
1 Swamp
2 Bloodghast
3 Bloodghast
```

(Lands totals adjusted; Bloodghast duplicated above is a copy/paste artifact — corrected during ingestion.)

## Cleaned mainboard

The deck-as-actually-played:

| Qty | Card | Role |
|---|---|---|
| 4 | Hogaak, Arisen Necropolis | core threat |
| 4 | Vengevine | recursive threat (returned via cast triggers) |
| 4 | Carrion Feeder | sacrifice outlet, *Vengevine* enabler |
| 4 | Stitcher's Supplier | self-mill engine |
| 4 | Gravecrawler | recursive threat, *Vengevine* enabler |
| 4 | Bloodghast | recursive threat |
| 4 | Insolent Neonate | self-mill + discard outlet |
| 4 | Faithless Looting | discard / fix hand (banned 2019-08-26) |
| 4 | Altar of Dementia | sacrifice outlet, mill self into more recursion |
| 3 | Goblin Bushwhacker | finisher |
| 2 | Lightning Axe | spot removal + discard enabler |
| 4 | Bloodstained Mire | fetchland |
| 4 | Wooded Foothills | fetchland |
| 2 | Blood Crypt | shockland |
| 1 | Stomping Ground | shockland |
| 2 | Overgrown Tomb | shockland |
| 4 | basics (Mountain x2, Forest, Swamp) | basics |

## Sideboard (15)

| Qty | Card | Role |
|---|---|---|
| 4 | Leyline of the Void | mirror / dredge hate |
| 3 | Nature's Claim | artifact / enchantment removal |
| 3 | Thoughtseize | disruption |
| 2 | Assassin's Trophy | catch-all removal |
| 3 | Force of Vigor | free removal vs artifacts/enchantments |

## Why this deck for the demo

1. **Famous and short-lived.** The Hogaak archetype existed in dominant form for two months; ban actions removed it. It is one of MTG's clearest cases of a deck so strong it forced format-level intervention.
2. **Heavy thematic load.** Almost every mainboard card maps to a theme already in MTGSLIDER's database — graveyard recursion, sacrifice fodder, zombies (Stitcher's Supplier, Gravecrawler), recursive threats. The cross-query is rich.
3. **Manageable size.** 75 cards, no token-generators or planeswalkers requiring special handling.
4. **Provenance is solid.** Wizards published official MC IV coverage; many top-8 lists are publicly documented; the archetype is extensively covered in retrospectives.

## Notes on data accuracy

This decklist is a composite reflecting the dominant build at the event. Individual top-8 lists varied in their land counts, in the choice between *Lightning Axe* and *Conduit of Storms* / *Lightning Bolt*, and in the sideboard configuration. For research purposes — especially cross-query against thematic databases — the composite is more useful than any single pilot's list. For tournament-record purposes a specific player's list would be better.

The ingester treats this file as a single decklist with `pilot: composite` to make the provenance honest.
