"""100 theme specs for bulk slide generation.

Each spec is a dict:
- name: human-readable theme name (becomes slug)
- description: one-line description
- query: Scryfall query string
- backend: "v1" | "compiler"
- style: optional compiler preset ("rhystic" | "sierkovitz" | "teaching")
- aliases: optional list of search aliases

Backend choice rule of thumb:
- sierkovitz for "X that do Y" mechanical themes (data slide adds value)
- rhystic for evocative flavor themes (visual motif slide adds value)
- teaching for "intro to X" beginner-friendly themes (takeaways slide adds value)

Queries use Scryfall syntax: https://scryfall.com/docs/syntax
We bias toward queries that return between ~5 and ~30 cards — too few cards
makes the deck thin, too many overwhelms the curation step.
"""
from __future__ import annotations


def _t(name: str, description: str, query: str, *, backend: str = "compiler",
       style: str | None = None, aliases: list[str] | None = None) -> dict:
    return {
        "name": name,
        "description": description,
        "query": query,
        "backend": backend,
        "style": style,
        "aliases": aliases or [],
    }


# ---------- 1. Single creature-type primers (20) ----------
CREATURE_PRIMERS = [
    _t("Dogs primer", "An introduction to Dog creatures across Magic.",
       "t:dog t:creature", style="teaching"),
    _t("Cats primer", "An introduction to Cat creatures.",
       "t:cat t:creature", style="teaching"),
    _t("Wizards primer", "An introduction to Wizard creatures.",
       "t:wizard t:creature -t:legendary", style="teaching"),
    _t("Zombies primer", "An introduction to Zombie creatures.",
       "t:zombie t:creature -t:legendary", style="teaching"),
    _t("Goblins primer", "An introduction to Goblin creatures.",
       "t:goblin t:creature -t:legendary", style="teaching"),
    _t("Elves primer", "An introduction to Elf creatures.",
       "t:elf t:creature -t:legendary", style="teaching"),
    _t("Merfolk primer", "An introduction to Merfolk creatures.",
       "t:merfolk t:creature -t:legendary", style="teaching"),
    _t("Vampires primer", "An introduction to Vampire creatures.",
       "t:vampire t:creature -t:legendary", style="teaching"),
    _t("Dragons primer", "An introduction to Dragon creatures.",
       "t:dragon t:creature -t:legendary", style="teaching"),
    _t("Angels primer", "An introduction to Angel creatures.",
       "t:angel t:creature -t:legendary", style="teaching"),
    _t("Demons primer", "An introduction to Demon creatures.",
       "t:demon t:creature -t:legendary", style="teaching"),
    _t("Knights primer", "An introduction to Knight creatures.",
       "t:knight t:creature -t:legendary", style="teaching"),
    _t("Soldiers primer", "An introduction to Soldier creatures.",
       "t:soldier t:creature -t:legendary", style="teaching"),
    _t("Faeries primer", "An introduction to Faerie creatures.",
       "t:faerie t:creature -t:legendary", style="teaching"),
    _t("Spirits primer", "An introduction to Spirit creatures.",
       "t:spirit t:creature -t:legendary", style="teaching"),
    _t("Treefolk primer", "An introduction to Treefolk creatures.",
       "t:treefolk t:creature -t:legendary", style="teaching"),
    _t("Beasts primer", "An introduction to Beast creatures.",
       "t:beast t:creature -t:legendary", style="teaching"),
    _t("Pirates primer", "An introduction to Pirate creatures.",
       "t:pirate t:creature -t:legendary", style="teaching"),
    _t("Dinosaurs primer", "An introduction to Dinosaur creatures.",
       "t:dinosaur t:creature -t:legendary", style="teaching"),
    _t("Ninjas primer", "An introduction to Ninja creatures.",
       "t:ninja t:creature -t:legendary", style="teaching"),
]

# ---------- 2. Creature-type ∩ keyword (40) ----------
KEYWORD_INTERSECTIONS = [
    _t("Dogs with a keyword", "Dog creatures with at least one keyword ability.",
       "t:dog t:creature (kw:flying or kw:vigilance or kw:lifelink or kw:trample or kw:haste or kw:menace or kw:reach)",
       style="sierkovitz"),
    _t("Cats with deathtouch", "Cat creatures with deathtouch.",
       "t:cat t:creature kw:deathtouch", style="sierkovitz"),
    _t("Cats with lifelink", "Cat creatures with lifelink.",
       "t:cat t:creature kw:lifelink", style="sierkovitz"),
    _t("Knights with first strike", "Knight creatures with first strike.",
       "t:knight t:creature kw:first-strike", style="sierkovitz"),
    _t("Knights with vigilance", "Knight creatures with vigilance.",
       "t:knight t:creature kw:vigilance", style="sierkovitz"),
    _t("Angels with vigilance", "Angel creatures with vigilance.",
       "t:angel t:creature kw:vigilance", style="sierkovitz"),
    _t("Angels with lifelink", "Angel creatures with lifelink.",
       "t:angel t:creature kw:lifelink", style="sierkovitz"),
    _t("Vampires with lifelink", "Vampire creatures with lifelink.",
       "t:vampire t:creature kw:lifelink", style="sierkovitz"),
    _t("Vampires with flying", "Vampire creatures with flying.",
       "t:vampire t:creature kw:flying", style="sierkovitz"),
    _t("Dragons with haste", "Dragon creatures with haste.",
       "t:dragon t:creature kw:haste", style="sierkovitz"),
    _t("Dragons with trample", "Dragon creatures with trample.",
       "t:dragon t:creature kw:trample", style="sierkovitz"),
    _t("Demons with flying", "Demon creatures with flying.",
       "t:demon t:creature kw:flying", style="sierkovitz"),
    _t("Goblins with haste", "Goblin creatures with haste.",
       "t:goblin t:creature kw:haste", style="sierkovitz"),
    _t("Goblins with menace", "Goblin creatures with menace.",
       "t:goblin t:creature kw:menace", style="sierkovitz"),
    _t("Elves with reach", "Elf creatures with reach.",
       "t:elf t:creature kw:reach", style="sierkovitz"),
    _t("Faeries with flash", "Faerie creatures with flash.",
       "t:faerie t:creature kw:flash", style="sierkovitz"),
    _t("Spirits with flying", "Spirit creatures with flying.",
       "t:spirit t:creature kw:flying", style="sierkovitz"),
    _t("Spirits with flash", "Spirit creatures with flash.",
       "t:spirit t:creature kw:flash", style="sierkovitz"),
    _t("Beasts with trample", "Beast creatures with trample.",
       "t:beast t:creature kw:trample", style="sierkovitz"),
    _t("Pirates with menace", "Pirate creatures with menace.",
       "t:pirate t:creature kw:menace", style="sierkovitz"),
    _t("Wizards with flash", "Wizard creatures with flash.",
       "t:wizard t:creature kw:flash", style="sierkovitz"),
    _t("Wizards with prowess", "Wizard creatures with prowess.",
       "t:wizard t:creature kw:prowess", style="sierkovitz"),
    _t("Soldiers with vigilance", "Soldier creatures with vigilance.",
       "t:soldier t:creature kw:vigilance", style="sierkovitz"),
    _t("Soldiers with first strike", "Soldier creatures with first strike.",
       "t:soldier t:creature kw:first-strike", style="sierkovitz"),
    _t("Merfolk with islandwalk", "Merfolk creatures with islandwalk.",
       "t:merfolk t:creature o:'islandwalk'", style="sierkovitz"),
    _t("Zombies with menace", "Zombie creatures with menace.",
       "t:zombie t:creature kw:menace", style="sierkovitz"),
    _t("Zombies with deathtouch", "Zombie creatures with deathtouch.",
       "t:zombie t:creature kw:deathtouch", style="sierkovitz"),
    _t("Treefolk with reach", "Treefolk creatures with reach.",
       "t:treefolk t:creature kw:reach", style="sierkovitz"),
    _t("Hydras with trample", "Hydra creatures with trample.",
       "t:hydra t:creature kw:trample", style="sierkovitz"),
    _t("Sphinxes with flying", "Sphinx creatures with flying.",
       "t:sphinx t:creature kw:flying", style="sierkovitz"),
    _t("Birds with flying", "Bird creatures with flying.",
       "t:bird t:creature kw:flying", style="sierkovitz"),
    _t("Snakes with deathtouch", "Snake creatures with deathtouch.",
       "t:snake t:creature kw:deathtouch", style="sierkovitz"),
    _t("Spiders with reach", "Spider creatures with reach.",
       "t:spider t:creature kw:reach", style="sierkovitz"),
    _t("Rats with menace", "Rat creatures with menace.",
       "t:rat t:creature kw:menace", style="sierkovitz"),
    _t("Cats with first strike", "Cat creatures with first strike.",
       "t:cat t:creature kw:first-strike", style="sierkovitz"),
    _t("Dogs with vigilance", "Dog creatures with vigilance.",
       "t:dog t:creature kw:vigilance", style="sierkovitz"),
    _t("Dogs with lifelink", "Dog creatures with lifelink.",
       "t:dog t:creature kw:lifelink", style="sierkovitz"),
    _t("Samurai with bushido", "Samurai creatures with bushido.",
       "t:samurai t:creature o:bushido", style="sierkovitz"),
    _t("Slivers with keyword sharing", "Slivers that grant a keyword to all slivers.",
       "t:sliver t:creature (o:'all sliver' or o:'each sliver')", style="sierkovitz"),
    _t("Eldrazi with annihilator", "Eldrazi creatures with annihilator.",
       "t:eldrazi t:creature o:annihilator", style="sierkovitz"),
]

# ---------- 3. Creature-type ∩ mechanical concern (20) ----------
MECHANIC_INTERSECTIONS = [
    _t("Dogs that draw cards", "Dog creatures whose oracle text references drawing cards.",
       "t:dog t:creature o:'draw a card'", style="sierkovitz"),
    _t("Cats that gain life", "Cat creatures that gain life.",
       "t:cat t:creature o:'gain life'", style="sierkovitz"),
    _t("Wizards that draw cards", "Wizard creatures whose oracle text references drawing cards.",
       "t:wizard t:creature o:'draw a card'", style="sierkovitz"),
    _t("Wizards that mill", "Wizard creatures that mill cards.",
       "t:wizard t:creature o:mill", style="sierkovitz"),
    _t("Goblins that sacrifice", "Goblin creatures that sacrifice creatures.",
       "t:goblin t:creature o:sacrifice", style="sierkovitz"),
    _t("Zombies that recur", "Zombie creatures that return things from graveyards.",
       "t:zombie t:creature o:'return' o:graveyard", style="sierkovitz"),
    _t("Vampires that drain life", "Vampire creatures that drain or damage life.",
       "t:vampire t:creature o:'lose' o:life", style="sierkovitz"),
    _t("Elves that ramp", "Elf creatures that produce mana.",
       "t:elf t:creature o:'add' o:mana", style="sierkovitz"),
    _t("Merfolk that mill", "Merfolk creatures that mill cards.",
       "t:merfolk t:creature o:mill", style="sierkovitz"),
    _t("Spirits that flicker", "Spirit creatures with blink/flicker effects.",
       "t:spirit t:creature (o:exile o:return)", style="sierkovitz"),
    _t("Beasts that fight", "Beast creatures with fight or bite effects.",
       "t:beast t:creature o:fight", style="sierkovitz"),
    _t("Knights that exile", "Knight creatures that exile permanents.",
       "t:knight t:creature o:exile", style="sierkovitz"),
    _t("Soldiers that make tokens", "Soldier creatures that produce creature tokens.",
       "t:soldier t:creature o:'create' o:token", style="sierkovitz"),
    _t("Angels that gain life", "Angel creatures that gain life.",
       "t:angel t:creature o:'gain' o:life", style="sierkovitz"),
    _t("Demons that punish", "Demon creatures that force opponents to lose life or sacrifice.",
       "t:demon t:creature (o:'lose life' or o:'sacrifice')", style="sierkovitz"),
    _t("Faeries that bounce", "Faerie creatures that return things to hand.",
       "t:faerie t:creature o:'return' o:hand", style="sierkovitz"),
    _t("Treefolk that pump", "Treefolk creatures that grant +1/+1 or get bigger.",
       "t:treefolk t:creature o:'+1/+1'", style="sierkovitz"),
    _t("Pirates that steal", "Pirate creatures that take treasures or cards.",
       "t:pirate t:creature (o:treasure or o:steal or o:gain control)", style="sierkovitz"),
    _t("Dinosaurs with enrage", "Dinosaur creatures with the enrage ability.",
       "t:dinosaur t:creature o:enrage", style="sierkovitz"),
    _t("Ninjas with ninjutsu", "Ninja creatures with ninjutsu.",
       "t:ninja t:creature o:ninjutsu", style="sierkovitz"),
]

# ---------- 4. Flavor / motif themes (20) ----------
FLAVOR_THEMES = [
    _t("Books in Magic", "Cards depicting books, scrolls, and writing.",
       "o:book or o:tome or o:scroll", style="rhystic", aliases=["scrolls", "tomes"]),
    _t("Doors in Magic", "Cards involving doors, gates, and thresholds.",
       "o:door or o:gate or t:'door'", style="rhystic"),
    _t("Dreams in Magic", "Cards invoking dreams and sleep.",
       "o:dream or o:sleep or n:dream", style="rhystic"),
    _t("Masks in Magic", "Cards involving masks and disguise.",
       "n:mask or o:mask", style="rhystic"),
    _t("Libraries as places", "Cards naming libraries (the location, not the deck).",
       "n:library -n:'library of'", style="rhystic"),
    _t("Ruins in Magic", "Cards depicting or named for ruins.",
       "n:ruin or n:ruins", style="rhystic"),
    _t("Sea creatures", "Cards depicting sea life: krakens, leviathans, octopi.",
       "(t:kraken or t:leviathan or t:octopus or t:whale)", style="rhystic"),
    _t("Insects in Magic", "Insect-typed creatures.",
       "t:insect t:creature", style="rhystic"),
    _t("Bees and wasps", "Cards involving bees, wasps, or hornets.",
       "n:bee or n:wasp or n:hornet or t:insect o:flying", style="rhystic"),
    _t("Mushrooms and fungi", "Fungus-typed creatures and saproling makers.",
       "(t:fungus or o:saproling)", style="rhystic"),
    _t("Lab and alchemy", "Cards depicting alchemy, labs, and experiments.",
       "name:alchemist or name:laboratory or n:lab", style="rhystic", aliases=["alchemy", "labs"]),
    _t("Graveyard engines", "Cards that recur creatures from graveyards.",
       "o:'return' o:'creature' o:'graveyard'", style="sierkovitz"),
    _t("Equipment payoffs", "Cards that care about equipment.",
       "o:equipped or o:'whenever equipment'", style="sierkovitz"),
    _t("Aura payoffs", "Cards that care about auras.",
       "o:enchanted o:creature o:'whenever'", style="sierkovitz"),
    _t("Token producers", "Cards that create lots of creature tokens.",
       "o:'create' o:'creature tokens'", style="sierkovitz"),
    _t("Sacrifice fodder", "Cards that benefit from sacrificing creatures.",
       "o:sacrifice o:creature o:'whenever'", style="sierkovitz"),
    _t("Mill engines", "Cards that mill the opponent.",
       "o:'mill' (o:opponent or o:target player)", style="sierkovitz"),
    _t("Hexproof creatures", "Creatures with hexproof.",
       "t:creature kw:hexproof", style="sierkovitz"),
    _t("Indestructible creatures", "Creatures with indestructible.",
       "t:creature kw:indestructible", style="sierkovitz"),
    _t("Defenders that swing", "Defenders that can attack via abilities.",
       "kw:defender o:attack", style="sierkovitz"),
]

ALL = (
    CREATURE_PRIMERS
    + KEYWORD_INTERSECTIONS
    + MECHANIC_INTERSECTIONS
    + FLAVOR_THEMES
)

assert len(ALL) == 100, f"expected 100 specs, got {len(ALL)}"
