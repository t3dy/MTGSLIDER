"""Narrative planner. Turns a theme packet into an ordered list of ArgumentUnits.

The plan is preset-aware: each preset produces a measurably different shape.
"""
from __future__ import annotations

from typing import Any

from . import notes, stats
from .slide_types import ArgumentUnit


def plan(packet: dict, preset: dict[str, Any]) -> list[ArgumentUnit]:
    mode = preset.get("narrative_mode", "thematic")
    if mode == "argument-driven":
        units = _plan_sierkovitz(packet, preset)
    elif mode == "definition-first":
        units = _plan_teaching(packet, preset)
    else:
        units = _plan_rhystic(packet, preset)

    # Speaker notes are filled in here so each planner doesn't repeat the call.
    notes_mode = preset.get("speaker_notes_mode", "")
    if notes_mode:
        for u in units:
            if not u.speaker_notes:
                u.speaker_notes = notes.for_unit(
                    u.content, u.slide_type, mode=notes_mode, theme=packet["theme"]
                )
    return units


# ---------- rhystic: narrative essay ----------

def _plan_rhystic(packet: dict, preset: dict[str, Any]) -> list[ArgumentUnit]:
    theme = packet["theme"]
    units: list[ArgumentUnit] = []
    units.append(_thesis(theme, packet["generated_at"]))
    if theme["aliases"] or theme["short_description"]:
        units.append(_definition(theme))

    # Visual motif slide between framing and the spotlight tour.
    if preset["include_visual_motifs"] and packet["included"]:
        units.append(_visual_motif(theme, packet["included"][:8]))

    label = preset["spotlight_label_for_exemplars"]
    for card in packet["exemplars"]:
        units.append(_spotlight(card, label=label))

    cap = preset.get("spotlight_cap", 6)
    for card in packet["included"][:cap]:
        units.append(_spotlight(card, label=""))

    units.append(_conclusion(theme, packet["counts"]))
    units.append(_citations(packet["generator"]))
    return units


# ---------- sierkovitz: data-driven ----------

def _plan_sierkovitz(packet: dict, preset: dict[str, Any]) -> list[ArgumentUnit]:
    theme = packet["theme"]
    units: list[ArgumentUnit] = []
    units.append(_thesis(theme, packet["generated_at"]))

    # Lead with stats.
    if preset["include_data_slide"]:
        agg = stats.aggregate(packet)
        units.append(ArgumentUnit(
            slide_type="data",
            rhetorical_role="evidence",
            content={
                "title": f"{theme['canonical_name']} by the numbers",
                "stats": agg,
                "claim": "Distribution across the curated set.",
            },
        ))

    label = preset["spotlight_label_for_exemplars"]
    for card in packet["exemplars"]:
        units.append(_spotlight(card, label=label))

    # Cap individual spotlights tight; the rest get clustered densely.
    cap = preset.get("spotlight_cap", 3)
    spotlit = packet["included"][:cap]
    remaining = packet["included"][cap:]
    for card in spotlit:
        units.append(_spotlight(card, label=""))
    if remaining:
        units.append(ArgumentUnit(
            slide_type="cluster",
            rhetorical_role="evidence",
            content={
                "title": "Supporting cards",
                "cards": remaining[:9],  # 3x3 grid cap
                "claim": f"{len(remaining)} additional cards in the included set.",
            },
            evidence_refs=[c["scryfall_id"] for c in remaining[:9]],
        ))

    units.append(_conclusion(theme, packet["counts"]))
    units.append(_citations(packet["generator"]))
    return units


# ---------- teaching: definition-first, takeaways before conclusion ----------

def _plan_teaching(packet: dict, preset: dict[str, Any]) -> list[ArgumentUnit]:
    theme = packet["theme"]
    units: list[ArgumentUnit] = []
    units.append(_thesis(theme, packet["generated_at"]))

    # Definition before anything else.
    units.append(_definition(theme))

    # "What to look for" framed as an additional definition slide.
    units.append(ArgumentUnit(
        slide_type="definition",
        rhetorical_role="framing",
        content={
            "title": "What to look for",
            "definition": (
                f"A card belongs to {theme['canonical_name']} when its name, type, oracle text, "
                "or art makes the connection legible at a glance. Some cards are obvious; "
                "the interesting cases are the near-misses."
            ),
            "examples": [c["card_name"] for c in (packet["exemplars"] or packet["included"])[:3]],
        },
    ))

    if preset["include_visual_motifs"] and packet["included"]:
        units.append(_visual_motif(theme, packet["included"][:8]))

    label = preset["spotlight_label_for_exemplars"]
    for card in packet["exemplars"]:
        units.append(_spotlight(card, label=label))

    cap = preset.get("spotlight_cap", 4)
    for card in packet["included"][:cap]:
        units.append(_spotlight(card, label=""))

    if preset.get("include_takeaways"):
        units.append(ArgumentUnit(
            slide_type="key_takeaways",
            rhetorical_role="synthesis",
            content={
                "title": "Key takeaways",
                "takeaways": _takeaways_from_packet(packet),
            },
        ))

    units.append(_conclusion(theme, packet["counts"]))
    units.append(_citations(packet["generator"]))
    return units


# ---------- shared unit builders ----------

def _thesis(theme: dict, generated_at: str) -> ArgumentUnit:
    return ArgumentUnit(
        slide_type="thesis",
        rhetorical_role="framing",
        content={
            "title": theme["canonical_name"],
            "claim": theme["short_description"] or "A thematic survey.",
            "subtitle": generated_at,
        },
    )


def _definition(theme: dict) -> ArgumentUnit:
    return ArgumentUnit(
        slide_type="definition",
        rhetorical_role="framing",
        content={
            "title": "What we mean by this theme",
            "definition": theme["short_description"] or theme["canonical_name"],
            "examples": theme["aliases"],
        },
    )


def _visual_motif(theme: dict, cards: list[dict]) -> ArgumentUnit:
    return ArgumentUnit(
        slide_type="visual_motif",
        rhetorical_role="evidence",
        content={
            "title": f"Visual motifs across {theme['canonical_name']}",
            "cards": cards,
            "motif_description": "Selected for shared visual or flavor cues.",
        },
        evidence_refs=[c["scryfall_id"] for c in cards],
    )


def _spotlight(card: dict, *, label: str) -> ArgumentUnit:
    return ArgumentUnit(
        slide_type="card_spotlight",
        rhetorical_role="evidence",
        content={
            "card": card,
            "image_path": card.get("image_path"),
            "label": label,
            "claim": card.get("link_reason") or card.get("note") or "",
        },
        evidence_refs=[card["scryfall_id"]],
    )


def _conclusion(theme: dict, counts: dict) -> ArgumentUnit:
    return ArgumentUnit(
        slide_type="conclusion",
        rhetorical_role="synthesis",
        content={
            "title": "What we found",
            "claim": (
                f"{counts['exemplar']} exemplar and {counts['include']} included cards span "
                f"the {theme['canonical_name']} theme. {counts['uncertain']} more remain to review."
            ),
        },
    )


def _citations(generator: str) -> ArgumentUnit:
    return ArgumentUnit(
        slide_type="citations",
        rhetorical_role="navigation",
        content={
            "title": "Sources",
            "sources": [
                "Scryfall (https://scryfall.com)",
                "Card images and names © Wizards of the Coast",
                f"MTGSLIDER {generator}",
            ],
        },
    )


def _takeaways_from_packet(packet: dict) -> list[str]:
    theme = packet["theme"]
    counts = packet["counts"]
    out = [
        f"{theme['canonical_name']} spans {counts['exemplar'] + counts['include']} curated cards.",
    ]
    if packet["exemplars"]:
        names = ", ".join(c["card_name"] for c in packet["exemplars"][:3])
        out.append(f"The clearest examples are: {names}.")
    if counts["uncertain"]:
        out.append(f"{counts['uncertain']} candidates remain uncertain — review before publishing.")
    return out
