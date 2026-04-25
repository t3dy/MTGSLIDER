"""Compiler generator: planner → validation → renderer."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from ...packet import build_packet
from ...paths import theme_dir
from .planner import plan
from .presets import resolve
from .renderer import render
from .slide_types import validate_units


def build(slug: str, *, out_path: Optional[Path] = None, style: Optional[str] = None) -> Path:
    packet = build_packet(slug)
    preset = resolve(style)
    units = plan(packet, preset)
    errors = validate_units(units)
    if errors:
        raise ValueError(
            "compiler produced invalid argument units:\n  " + "\n  ".join(errors)
        )
    prs = render(units, preset)
    target = out_path or (theme_dir(slug) / "out" / f"{slug}.compiler.{preset.get('narrative_mode','default')}.pptx")
    target.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(target))
    return target
