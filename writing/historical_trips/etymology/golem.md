---
slug: golem
source_type: etymology
title: golem
summary: An artificial humanoid animated by ritual — Hebrew *gōlem* "shapeless mass", canonical in the Maharal of Prague legend; in MTG, a creature subtype indicating constructed, often animated artifact-bodies.
confidence: high
review_status: reviewed
mtg_card_refs: []
mtg_theme_refs: []
---

# golem

## First attestation (in English)

- **Earliest extant use:** the word *golem* enters English in the late 19th c. via translations and scholarly reports of Eastern European Jewish folklore. The OED records 1897.
- **Form:** transliteration of Hebrew גֹּלֶם.
- **Glossing:** "an artificial human figure animated by Kabbalistic ritual; figuratively, an automaton, a brute mass."

## Source-language chain

| Language | Original form | Transliteration | Gloss | Earliest extant date |
|---|---|---|---|---|
| Hebrew | גֹּלֶם | *gōlem* | "shapeless mass, unfinished thing" — Psalm 139:16 has the only biblical occurrence | composition of Psalms, post-exilic |
| Mishnaic Hebrew | גולם | *golem* | "an unformed person; a clod" — figurative, applied to those who lack social grace | Tannaitic period (1st–2nd c. CE) |
| Medieval Hebrew (Kabbalah) | גולם | *golem* | "an artificial creature animated by manipulation of divine names" — the *Sefer Yetzirah* tradition | from the *Sefer Yetzirah* (composed somewhere between 200 BCE and 200 CE), elaborated by Jewish mystics through the medieval period |

The word itself is biblical; the *technical* sense — an artificial creature animated by ritual — is Kabbalistic, attaching to the *Sefer Yetzirah* (the "Book of Formation") and elaborated by Eleazar of Worms (c. 1176 – c. 1238) and others. The Maharal of Prague (Rabbi Judah Loew ben Bezalel, c. 1525–1609) is the legendary creator of the most famous golem; the legend itself crystallises in print in Yudl Rosenberg's *Niflo'es Maharal* (1909), a literary work that established the modern shape of the story.

## Cognates and cousins

| Cognate | Language | Relation | Note |
|---|---|---|---|
| *Golem* | German | direct loan | central to Gustav Meyrink's novel *Der Golem* (1915) |
| *Glem* | Yiddish | direct descendant | colloquial use survives |
| no Indo-European cognates | — | — | Hebrew root *g-l-m* is Semitic; the broad family of "automaton" terms (*automaton* itself, Greek; *robot*, Czech) are independent formations |

## Period definitions

| Period | Definition | Source |
|---|---|---|
| Biblical | "shapeless thing; embryo" — a single occurrence in Psalm 139:16 | Hebrew Bible |
| Mishnaic / Talmudic | "an uncultured person; a clod" — figurative | Mishnah, *Pirkei Avot* 5:7 |
| Medieval Kabbalistic | "an artificial creature animated by ritual manipulation of divine names" | the *Sefer Yetzirah* tradition; Eleazar of Worms |
| Modern (post-1909) | "a humanoid figure animated by Kabbalistic art; (transferred) any constructed quasi-living thing" | Yudl Rosenberg, *Niflo'es Maharal* (1909); Gustav Meyrink, *Der Golem* (1915) |

## Semantic shift

Three discrete jumps. (1) Biblical *unformed thing* → Talmudic *uncultured person* — an extension of the "without form" sense to social character. (2) Talmudic figurative → medieval technical: the Kabbalists make the word a term of art for an artificial being. (3) Eastern European Jewish folklore → modern world literature: Rosenberg's print version and Meyrink's novel fix the figure for non-Jewish readers, and from there it enters the Western fantasy lexicon (and eventually D&D, MTG, video games).

## MTG use

- **Card-text use:** Golem is a creature subtype, applied almost exclusively to artifact creatures. First appearances include *Clay Statue* (Alpha) — though the explicit Golem subtype was added later in retroactive errata. Significant Golems include *Phyrexian Colossus*, *Sundering Titan*, *Wurmcoil Engine* (a Wurm, not a Golem, but the design lineage is shared), *Karn Liberated* (Golem-typed planeswalker character), *Memnarch*.
- **Flavor use:** MTG Golems are almost always *constructed by a named artificer* — Urza, Mishra, Karn (himself a Golem), the Phyrexians. The Mirrodin block (2003) is the densest Golem set.
- **Representative cards:** *Wurmcoil Engine* (technically a Wurm, but the design family), *Sundering Titan*, *Phyrexian Colossus*, *Memnarch*, *Karn Liberated*.

## MTG connection

MTG's Golems preserve the *constructed-and-animated* sense almost without modification — every Golem in the game has a maker. The Kabbalistic association (animation through inscribed names) is occasionally cited in flavor text but is not load-bearing. The closest direct citation is the older flavor convention of inscribing names on artifact creatures (the *Mishra's Workshop* / Antiquities tradition), which is structurally analogous to the *Maharal* writing the divine name on the golem's forehead — but MTG does not press the analogy. The connection is iconographic, not theological.

## Sources

- *Sefer Yetzirah* (English: Aryeh Kaplan, *Sefer Yetzirah: The Book of Creation* (Weiser, 1990))
- Gershom Scholem, *On the Kabbalah and Its Symbolism* (Schocken, 1965), ch. 5 "The Idea of the Golem"
- Moshe Idel, *Golem: Jewish Magical and Mystical Traditions on the Artificial Anthropoid* (SUNY Press, 1990)
- Yudl Rosenberg, *Niflo'es Maharal* (1909) — the literary crystallisation
- OED s.v. *golem*

## Wire-in commands

```bash
PYTHONPATH=src python -m mtgslider theme create "Golem — a historical trip"
PYTHONPATH=src python -m mtgslider theme find-cards "golem-a-historical-trip" --query 't:golem t:creature -t:legendary'
```
