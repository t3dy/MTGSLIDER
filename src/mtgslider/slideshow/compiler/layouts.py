"""Layout registry. Each layout declares slot structure and slide-type compatibility."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from pptx.util import Inches, Pt


@dataclass
class Layout:
    name: str
    compatible_slide_types: tuple[str, ...]
    max_content_density: int  # rough cap on words shown
    typography_scale: float = 1.0
    description: str = ""


LAYOUT_REGISTRY: dict[str, Layout] = {
    "single_image_focus": Layout(
        name="single_image_focus",
        compatible_slide_types=("card_spotlight",),
        max_content_density=40,
        description="One image left, claim+caption right",
    ),
    "split_image_text": Layout(
        name="split_image_text",
        compatible_slide_types=("card_spotlight", "definition"),
        max_content_density=80,
        description="Image left, body text right (more text than focus layout)",
    ),
    "grid_2x2": Layout(
        name="grid_2x2",
        compatible_slide_types=("cluster", "visual_motif"),
        max_content_density=120,
        description="2x2 grid of cards with title bar",
    ),
    "cluster_grid_dense": Layout(
        name="cluster_grid_dense",
        compatible_slide_types=("cluster",),
        max_content_density=200,
        description="3x3 grid for dense card surveys (Sierkovitz-style)",
    ),
    "data_chart_text": Layout(
        name="data_chart_text",
        compatible_slide_types=("data",),
        max_content_density=160,
        description="Stats table on left, claim on right",
    ),
    "takeaways": Layout(
        name="takeaways",
        compatible_slide_types=("key_takeaways",),
        max_content_density=100,
        typography_scale=1.2,
        description="Numbered key takeaways list",
    ),
    "text_only": Layout(
        name="text_only",
        compatible_slide_types=("thesis", "definition", "transition", "conclusion", "citations"),
        max_content_density=80,
        typography_scale=1.4,
        description="Centered text, no image",
    ),
}


def select_layout(slide_type: str, *, density: str = "medium") -> Layout:
    """Pick the layout for a slide type. `density` biases toward sparser or denser layouts."""
    candidates = [l for l in LAYOUT_REGISTRY.values() if slide_type in l.compatible_slide_types]
    if not candidates:
        return LAYOUT_REGISTRY["text_only"]  # safe fallback
    if density == "low":
        return min(candidates, key=lambda l: l.max_content_density)
    if density == "high":
        return max(candidates, key=lambda l: l.max_content_density)
    # medium: pick the first declared
    return candidates[0]
