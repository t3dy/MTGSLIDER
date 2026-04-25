"""Semantic slide types as argument units."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

# Slide type → required / optional content keys.
SLIDE_TYPE_SCHEMA: dict[str, dict[str, list[str]]] = {
    "thesis": {
        "required": ["title", "claim"],
        "optional": ["subtitle"],
    },
    "definition": {
        "required": ["title", "definition"],
        "optional": ["examples"],
    },
    "card_spotlight": {
        "required": ["card"],
        "optional": ["claim", "image_path", "label"],
    },
    "cluster": {
        "required": ["title", "cards"],
        "optional": ["claim"],
    },
    "visual_motif": {
        "required": ["title", "cards"],
        "optional": ["motif_description"],
    },
    "data": {
        "required": ["title", "stats"],
        "optional": ["claim"],
    },
    "key_takeaways": {
        "required": ["title", "takeaways"],
        "optional": [],
    },
    "transition": {
        "required": ["title"],
        "optional": ["subtitle"],
    },
    "conclusion": {
        "required": ["title", "claim"],
        "optional": ["next_steps"],
    },
    "citations": {
        "required": ["title"],
        "optional": ["sources"],
    },
}


@dataclass
class ArgumentUnit:
    """One slide as an argument unit. Layout is decided by the renderer, not here."""
    slide_type: str
    rhetorical_role: str  # e.g. "framing", "evidence", "synthesis", "navigation"
    content: dict[str, Any] = field(default_factory=dict)
    evidence_refs: list[str] = field(default_factory=list)  # scryfall_ids, source URLs, etc.
    speaker_notes: str = ""

    def validate(self) -> list[str]:
        errors: list[str] = []
        schema = SLIDE_TYPE_SCHEMA.get(self.slide_type)
        if schema is None:
            return [f"unknown slide_type {self.slide_type!r}"]
        for key in schema["required"]:
            if key not in self.content or self.content[key] in (None, "", [], {}):
                errors.append(f"slide_type={self.slide_type!r} missing required field {key!r}")
        return errors


def validate_units(units: list[ArgumentUnit]) -> list[str]:
    errors: list[str] = []
    for i, u in enumerate(units):
        for err in u.validate():
            errors.append(f"unit[{i}]: {err}")
    return errors
