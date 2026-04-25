"""Theme packet exporter. Same data, two surfaces: JSON (for slideshow backends) and Markdown (for human review)."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from . import __version__
from .db import connect
from .paths import theme_dir
from .themes import get_theme, list_images, list_links


def build_packet(
    slug: str,
    *,
    conn: Optional[sqlite3.Connection] = None,
) -> dict:
    own_conn = conn is None
    conn = conn or connect()
    try:
        theme = get_theme(slug, conn=conn)
        all_links = list_links(slug, conn=conn)
        images = list_images(slug, conn=conn)
        # index images by scryfall_id+face_index for fast lookup
        img_index: dict[tuple[str, int], dict] = {}
        for img in images:
            img_index[(img["scryfall_id"], img["face_index"])] = img

        def bucketed(status: str) -> list[dict]:
            return [_link_to_card_entry(l, img_index) for l in all_links if l["include_status"] == status]

        return {
            "schema_version": 1,
            "generator": f"mtgslider/{__version__}",
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "theme": {
                "slug": theme["slug"],
                "canonical_name": theme["canonical_name"],
                "short_description": theme["short_description"],
                "research_status": theme["research_status"],
                "aliases": theme["aliases"],
            },
            "counts": {
                "total_links": len(all_links),
                "exemplar": len(bucketed("exemplar")),
                "include": len(bucketed("include")),
                "uncertain": len(bucketed("uncertain")),
                "exclude": len(bucketed("exclude")),
                "with_images": sum(1 for l in all_links if (l["scryfall_id"], 0) in img_index),
            },
            "exemplars": bucketed("exemplar"),
            "included": bucketed("include"),
            "uncertain": bucketed("uncertain"),
            "excluded": bucketed("exclude"),
        }
    finally:
        if own_conn:
            conn.close()


def _link_to_card_entry(link: dict, img_index: dict) -> dict:
    img = img_index.get((link["scryfall_id"], 0))
    return {
        "scryfall_id": link["scryfall_id"],
        "card_name": link["card_name"],
        "type_line": link["type_line"],
        "mana_cost": link["mana_cost"],
        "include_status": link["include_status"],
        "review_status": link["review_status"],
        "link_type": link["link_type"],
        "link_reason": link["link_reason"],
        "confidence": link["confidence"],
        "note": link["note"],
        "image_path": img["local_path"] if img else None,
        "image_variant": img["variant"] if img else None,
        "image_source_url": img["source_url"] if img else None,
    }


def write_packet(slug: str, *, conn: Optional[sqlite3.Connection] = None) -> tuple[Path, Path]:
    packet = build_packet(slug, conn=conn)
    out_dir = theme_dir(slug) / "out"
    json_path = out_dir / "packet.json"
    md_path = out_dir / "packet.md"
    json_path.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    md_path.write_text(_render_markdown(packet), encoding="utf-8")
    return json_path, md_path


def _render_markdown(packet: dict) -> str:
    t = packet["theme"]
    lines: list[str] = []
    lines.append(f"# Theme: {t['canonical_name']}")
    lines.append("")
    lines.append(f"- **Slug:** `{t['slug']}`")
    lines.append(f"- **Status:** {t['research_status']}")
    if t["aliases"]:
        lines.append(f"- **Aliases:** {', '.join(t['aliases'])}")
    if t["short_description"]:
        lines.append(f"- **Description:** {t['short_description']}")
    lines.append(f"- **Generated:** {packet['generated_at']}")
    lines.append(f"- **Generator:** {packet['generator']}")
    lines.append("")
    c = packet["counts"]
    lines.append(
        f"**Counts:** {c['exemplar']} exemplar · {c['include']} included · "
        f"{c['uncertain']} uncertain · {c['exclude']} excluded · "
        f"{c['with_images']}/{c['total_links']} with images"
    )
    lines.append("")

    for header, key in (
        ("Exemplars", "exemplars"),
        ("Included", "included"),
        ("Uncertain", "uncertain"),
        ("Excluded", "excluded"),
    ):
        cards = packet[key]
        if not cards:
            continue
        lines.append(f"## {header} ({len(cards)})")
        lines.append("")
        for c in cards:
            lines.append(f"### {c['card_name']}")
            lines.append(f"- {c['type_line']}  {c['mana_cost']}")
            lines.append(f"- Link: `{c['link_type']}` — {c['link_reason']} (conf {c['confidence']:.2f})")
            if c["note"]:
                lines.append(f"- Note: {c['note']}")
            if c["image_path"]:
                lines.append(f"- Image: `{c['image_path']}` ({c['image_variant']})")
            lines.append("")
    return "\n".join(lines)
