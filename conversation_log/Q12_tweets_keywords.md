# Q12 — 100 topics from tweets for MTG's most magical keywords

## Verbatim user input

> look into my tweets on historical magic and alchemy to generate 100 topics for deep dives into the background of magic's 100 most magical keywords

## How I interpreted it

Two parts: (1) mine tweets, (2) produce 100 keyword-deep-dive topics.

Tweet archive: checked `C:\Dev\SocialsDB` — claims to integrate Twitter/Megabase/Claude/SMS, but the metadata shows only `twitter: 1` entry and there is no `.db` file present. The tweet corpus is not currently accessible. Did not invent tweet content.

Decided to deliver the 100-topic list deterministically (without tweets) — Magic's keyword vocabulary is bounded and well-known, so a useful list can be generated from Scryfall's keyword index plus the game's vocabulary of magical action verbs. Parked the tweet-mining piece for when an archive is available.

## What I built

[writing/100_magical_keywords.md](../writing/100_magical_keywords.md) — 100 keyword topics in five thematic groups:
- A. Action verbs that name a magical operation (24): conjure, sorcery, cantrip, scry, surveil, divinate, summon, banish, exile, manifest, foretell, transmute, transform, meld, morph, proliferate, populate, adapt, mutate, regenerate, reanimate, enchant, curse, bless
- B. Evergreen keyword abilities (20): flying, first strike, deathtouch, lifelink, trample, vigilance, haste, hexproof, indestructible, menace, reach, ward, defender, prowess, flash, scry, mill, shroud, protection
- C. Deciduous/historical keywords (28): cascade, undying, persist, dredge, threshold, madness, flashback, storm, unleash, bestow, heroic, devotion, constellation, inspired, tribute, convoke, extort, exalted, landfall, annihilator, infect, metalcraft, living weapon, bushido, ninjutsu, soulshift, channel
- D. Magical-material actions (12): sacrifice, tap, untap, counter (verb/noun), mana, venture, gift, conspire, imprint, echo
- E. Mechanics named after esoteric concepts (16): spellbook, familiar, leyline, sigil, rune, glyph, wraith, specter, phantasm, golem, homunculus, elemental, lich, ooze, demon, angel

Each row has a "why it earns a trip" note pointing at the historical/esoteric register. Designed to be fed to the `mtg-historical-trip` skill in batches of 12.

Parked tweet-archive mining in `PARKING_LOT.md` — re-rank the keyword list by tweet attention/sentiment when a tweet archive becomes available.

## What I deferred

Tweet-archive mining (no accessible data). Parked in `PARKING_LOT.md` with prerequisite: locate or import a tweet archive into a queryable form.
