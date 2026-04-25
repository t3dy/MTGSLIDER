"""Style presets. Each preset is a config dict that influences planning and rendering.

A preset is the contract between a creator's voice and the compiler. Changes here
should produce visibly different decks — if two presets produce identical output,
they don't deserve to be separate presets.
"""
from __future__ import annotations

from typing import Any

PRESETS: dict[str, dict[str, Any]] = {
    "rhystic": {
        # Narrative essay voice. Image-rich, sparse text, visual motif emphasis.
        "narrative_mode": "thematic",
        "density": "low",
        "image_priority": "high",
        "include_visual_motifs": True,
        "include_data_slide": False,
        "include_takeaways": False,
        "max_words_per_slide": 35,
        "spotlight_label_for_exemplars": "EXEMPLAR",
        "spotlight_cap": 6,
        "use_dense_clusters": False,
        "speaker_notes_mode": "rich",   # full essay-voice prose
        "evidence_mode": "clean",       # no citation footers on slides
    },
    "sierkovitz": {
        # Data-driven analyst voice. Skip flavor, lead with stats, cluster densely.
        "narrative_mode": "argument-driven",
        "density": "high",
        "image_priority": "medium",
        "include_visual_motifs": False,
        "include_data_slide": True,
        "include_takeaways": False,
        "max_words_per_slide": 100,
        "spotlight_label_for_exemplars": "KEY CARD",
        "spotlight_cap": 3,             # fewer hero slides — clusters do the work
        "use_dense_clusters": True,     # 3x3 grids of remaining cards
        "speaker_notes_mode": "terse",  # brief factual notes
        "evidence_mode": "annotated",   # citation footers visible
    },
    "teaching": {
        # Pedagogical voice. Definition-first, example-driven, takeaways before conclusion.
        "narrative_mode": "definition-first",
        "density": "medium",
        "image_priority": "high",
        "include_visual_motifs": True,
        "include_data_slide": False,
        "include_takeaways": True,
        "max_words_per_slide": 65,
        "spotlight_label_for_exemplars": "EXAMPLE",
        "spotlight_cap": 4,
        "use_dense_clusters": False,
        "speaker_notes_mode": "heuristic",  # "when you see X, think Y"
        "evidence_mode": "annotated",
    },
}

DEFAULT_PRESET = "rhystic"


def resolve(preset_name: str | None) -> dict[str, Any]:
    name = preset_name or DEFAULT_PRESET
    if name not in PRESETS:
        raise ValueError(f"unknown preset {name!r}; available: {sorted(PRESETS)}")
    return dict(PRESETS[name])
