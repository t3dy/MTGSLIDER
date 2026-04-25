"""Bulk theme generator. Resumable, polite to Scryfall, writes a CSV index.

Usage:
    python tools/bulk_generate.py [--limit N] [--start-from IDX] [--no-images]

Per theme:
    1. Create theme (skip if exists)
    2. Run Scryfall query, stage up to STAGED_PER_THEME cards
    3. Mark first 2 as exemplar, next 3 as include
    4. Fetch images for those 5 (unless --no-images)
    5. Build packet
    6. Generate one .pptx in the chosen backend/style
    7. Append a row to bulk_index.csv

Skips themes with zero Scryfall results (logged in bulk_skipped.csv).
"""
from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.theme_specs import ALL  # noqa: E402

from mtgslider import themes  # noqa: E402
from mtgslider.db import connect  # noqa: E402
from mtgslider.packet import write_packet  # noqa: E402
from mtgslider.paths import theme_dir  # noqa: E402

STAGED_PER_THEME = 20
EXEMPLAR_COUNT = 2
INCLUDE_COUNT = 3
IMAGE_VARIANT = "normal"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=None, help="Only process the first N specs")
    p.add_argument("--start-from", type=int, default=0, help="Start at this index (0-based)")
    p.add_argument("--no-images", action="store_true", help="Skip image downloads")
    args = p.parse_args()

    specs = ALL[args.start_from:]
    if args.limit:
        specs = specs[: args.limit]

    out_root = ROOT / "themes"
    out_root.mkdir(parents=True, exist_ok=True)
    index_path = out_root / "bulk_index.csv"
    skipped_path = out_root / "bulk_skipped.csv"

    index_existing_slugs = _read_existing_slugs(index_path)
    index_file = index_path.open("a", newline="", encoding="utf-8")
    skipped_file = skipped_path.open("a", newline="", encoding="utf-8")
    iw = csv.writer(index_file)
    sw = csv.writer(skipped_file)
    if index_path.stat().st_size == 0:
        iw.writerow(["index", "slug", "name", "backend", "style", "staged", "pptx_path"])
    if skipped_path.stat().st_size == 0:
        sw.writerow(["index", "slug", "name", "reason"])

    n_done = n_skipped = n_failed = 0
    try:
        for i, spec in enumerate(specs, start=args.start_from):
            slug = themes.slugify(spec["name"])
            print(f"[{i+1:3d}/{args.start_from + len(specs):3d}] {spec['name']!s:45s}", flush=True)
            if slug in index_existing_slugs:
                print(f"        SKIP — already in index")
                n_skipped += 1
                continue
            try:
                result = _process(spec, fetch_images=not args.no_images)
            except Exception as e:
                print(f"        FAILED — {e}")
                traceback.print_exc()
                sw.writerow([i, slug, spec["name"], f"exception: {e}"])
                skipped_file.flush()
                n_failed += 1
                continue
            if result is None:
                print(f"        SKIP — zero Scryfall results")
                sw.writerow([i, slug, spec["name"], "zero results"])
                skipped_file.flush()
                n_skipped += 1
                continue
            staged, pptx_path = result
            iw.writerow([i, slug, spec["name"], spec["backend"], spec.get("style") or "", staged, str(pptx_path)])
            index_file.flush()
            print(f"        OK — {staged} staged, wrote {pptx_path.name}")
            n_done += 1
    finally:
        index_file.close()
        skipped_file.close()

    print()
    print(f"done.  ok={n_done}  skipped={n_skipped}  failed={n_failed}")
    print(f"index: {index_path}")
    return 0


def _process(spec: dict, *, fetch_images: bool) -> tuple[int, Path] | None:
    slug = themes.slugify(spec["name"])
    # Idempotent create.
    try:
        theme = themes.get_theme(slug)
    except KeyError:
        theme = themes.create_theme(
            spec["name"],
            short_description=spec.get("description"),
            aliases=spec.get("aliases", []),
        )

    staged = themes.find_cards_by_query(slug, spec["query"], limit=STAGED_PER_THEME)
    if staged == 0 and not themes.list_links(slug):
        return None

    links = themes.list_links(slug)
    # Auto-curate top results without manual review.
    for link in links[:EXEMPLAR_COUNT]:
        themes.mark_card(slug, link["card_name"], include_status="exemplar")
    for link in links[EXEMPLAR_COUNT:EXEMPLAR_COUNT + INCLUDE_COUNT]:
        themes.mark_card(slug, link["card_name"], include_status="include")

    if fetch_images:
        themes.fetch_images_for_theme(slug, variant=IMAGE_VARIANT)

    write_packet(slug)

    backend = spec.get("backend", "compiler")
    style = spec.get("style")
    if backend == "v1":
        from mtgslider.slideshow.v1_template.generator import build as build_v1
        path = build_v1(slug)
    else:
        from mtgslider.slideshow.compiler.generator import build as build_compiler
        path = build_compiler(slug, style=style)
    return staged, path


def _read_existing_slugs(index_path: Path) -> set[str]:
    if not index_path.exists():
        return set()
    out: set[str] = set()
    with index_path.open(encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            slug = row.get("slug")
            if slug:
                out.add(slug)
    return out


if __name__ == "__main__":
    raise SystemExit(main())
