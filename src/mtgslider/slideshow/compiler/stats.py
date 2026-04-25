"""Aggregate statistics over a theme packet. Used by the data slide."""
from __future__ import annotations

import re
from collections import Counter
from typing import Any


_MANA_PIP = re.compile(r"\{([^}]+)\}")
_NUMERIC_PIP = re.compile(r"^\d+$")


def aggregate(packet: dict, *, statuses: tuple[str, ...] = ("exemplar", "include")) -> dict[str, Any]:
    """Compute color, type, and mana-value distributions over the chosen buckets."""
    cards: list[dict] = []
    for s in statuses:
        cards.extend(packet.get({"exemplar": "exemplars", "include": "included"}.get(s, s + "s"), []))

    color_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    mv_counts: Counter[int] = Counter()
    for card in cards:
        for c in _colors(card):
            color_counts[c] += 1
        type_counts[_primary_type(card.get("type_line", ""))] += 1
        mv_counts[_mana_value(card.get("mana_cost", ""))] += 1

    return {
        "card_count": len(cards),
        "by_color": _ordered(color_counts, ["W", "U", "B", "R", "G", "C"]),
        "by_type": _ordered(type_counts, ["Creature", "Instant", "Sorcery", "Artifact", "Enchantment", "Land", "Planeswalker", "Other"]),
        "by_mana_value": dict(sorted(mv_counts.items())),
    }


def _colors(card: dict) -> list[str]:
    # Card dicts in the packet flatten oracle-level color info; fall back to "C" for colorless.
    # The packet entries don't currently carry full color list, so derive from mana_cost as a proxy.
    pips = _MANA_PIP.findall(card.get("mana_cost", "") or "")
    out: set[str] = set()
    for pip in pips:
        for ch in pip.upper():
            if ch in {"W", "U", "B", "R", "G"}:
                out.add(ch)
    return sorted(out) if out else ["C"]


def _primary_type(type_line: str) -> str:
    t = type_line.lower()
    for kw in ("creature", "instant", "sorcery", "artifact", "enchantment", "land", "planeswalker"):
        if kw in t:
            return kw.capitalize()
    return "Other"


def _mana_value(mana_cost: str) -> int:
    mv = 0
    for pip in _MANA_PIP.findall(mana_cost or ""):
        if _NUMERIC_PIP.match(pip):
            mv += int(pip)
        elif pip.upper() == "X":
            continue  # X contributes 0 by Scryfall convention
        else:
            mv += 1  # any colored or hybrid pip counts as 1
    return mv


def _ordered(counter: Counter, order: list[str]) -> dict[str, int]:
    out = {k: counter.get(k, 0) for k in order if counter.get(k, 0) > 0}
    # Then any leftovers not in `order`
    for k, v in counter.items():
        if k not in out and v > 0:
            out[k] = v
    return out
