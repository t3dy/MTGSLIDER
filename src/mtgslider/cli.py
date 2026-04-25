"""CLI surface for mtgslider.

Subcommands:
  theme create <name> [--alias ...] [--description ...]
  theme list
  theme show <slug>
  theme find-cards <slug> --query <scryfall-query> [--limit N]
  theme add <slug> <card-name>            # manual add as 'include'
  theme list-cards <slug> [--status S]
  theme mark <slug> <card-name> [--status S] [--review reviewed|unreviewed] [--note ...]
  theme fetch-images <slug> [--variant V] [--all]
  theme packet <slug>                     # writes packet.json + packet.md
  slides build <slug> --backend v1|compiler [--out PATH]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .images import DEFAULT_VARIANT, VARIANTS
from .packet import write_packet
from . import themes


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mtgslider", description="MTG thematic research and slideshow pipeline")
    sub = p.add_subparsers(dest="group", required=True)

    # theme group
    theme = sub.add_parser("theme", help="theme commands")
    tsub = theme.add_subparsers(dest="cmd", required=True)

    t_create = tsub.add_parser("create", help="create a new theme")
    t_create.add_argument("name")
    t_create.add_argument("--alias", action="append", default=[])
    t_create.add_argument("--description", default=None)

    tsub.add_parser("list", help="list themes")

    t_show = tsub.add_parser("show", help="show a theme")
    t_show.add_argument("slug")

    t_find = tsub.add_parser("find-cards", help="search Scryfall and stage candidates")
    t_find.add_argument("slug")
    t_find.add_argument("--query", required=True, help="Scryfall query syntax")
    t_find.add_argument("--limit", type=int, default=None)

    t_add = tsub.add_parser("add", help="manually add a card by name (marks include)")
    t_add.add_argument("slug")
    t_add.add_argument("card_name")
    t_add.add_argument("--status", default="include", choices=["include", "exclude", "uncertain", "exemplar"])
    t_add.add_argument("--exact", action="store_true", help="exact name match (default fuzzy)")

    t_list_cards = tsub.add_parser("list-cards", help="list cards linked to a theme")
    t_list_cards.add_argument("slug")
    t_list_cards.add_argument("--status", default=None, choices=["include", "exclude", "uncertain", "exemplar"])

    t_mark = tsub.add_parser("mark", help="set include/review status for a card")
    t_mark.add_argument("slug")
    t_mark.add_argument("card_name")
    t_mark.add_argument("--status", default=None, choices=["include", "exclude", "uncertain", "exemplar"])
    t_mark.add_argument("--review", default=None, choices=["reviewed", "unreviewed"])
    t_mark.add_argument("--note", default=None)

    t_imgs = tsub.add_parser("fetch-images", help="download card images for the theme")
    t_imgs.add_argument("slug")
    t_imgs.add_argument("--variant", default=DEFAULT_VARIANT, choices=list(VARIANTS))
    t_imgs.add_argument("--all", action="store_true", help="include uncertain cards too")

    t_packet = tsub.add_parser("packet", help="write packet.json and packet.md")
    t_packet.add_argument("slug")

    # slides group
    slides = sub.add_parser("slides", help="slideshow commands")
    ssub = slides.add_subparsers(dest="cmd", required=True)
    s_build = ssub.add_parser("build", help="generate a .pptx for a theme")
    s_build.add_argument("slug")
    s_build.add_argument("--backend", required=True, choices=["v1", "compiler"])
    s_build.add_argument("--out", default=None, help="output .pptx path (default: themes/<slug>/out/)")
    s_build.add_argument("--style", default=None, help="(compiler only) style preset: rhystic|sierkovitz|teaching")

    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.group == "theme":
        return _dispatch_theme(args)
    if args.group == "slides":
        return _dispatch_slides(args)
    parser.print_help()
    return 1


def _dispatch_theme(args: argparse.Namespace) -> int:
    if args.cmd == "create":
        t = themes.create_theme(args.name, short_description=args.description, aliases=args.alias)
        print(f"created theme: {t['slug']}")
        return 0
    if args.cmd == "list":
        for t in themes.list_themes():
            print(f"{t['slug']:30s}  {t['research_status']:18s}  {t['canonical_name']}")
        return 0
    if args.cmd == "show":
        t = themes.get_theme(args.slug)
        print(json.dumps(t, indent=2))
        return 0
    if args.cmd == "find-cards":
        n = themes.find_cards_by_query(args.slug, args.query, limit=args.limit)
        print(f"staged {n} cards from query: {args.query}")
        return 0
    if args.cmd == "add":
        card = themes.add_card_by_name(args.slug, args.card_name, fuzzy=not args.exact, include_status=args.status)
        if card is None:
            print(f"no Scryfall match for {args.card_name!r}", file=sys.stderr)
            return 2
        print(f"added: {card.name} ({card.set_code.upper()}) as {args.status}")
        return 0
    if args.cmd == "list-cards":
        for link in themes.list_links(args.slug, include_status=args.status):
            marker = {"exemplar": "*", "include": "+", "uncertain": "?", "exclude": "-"}.get(
                link["include_status"], " "
            )
            print(f"{marker} [{link['include_status']:9s}] {link['card_name']:40s}  {link['type_line']}")
        return 0
    if args.cmd == "mark":
        n = themes.mark_card(
            args.slug,
            args.card_name,
            include_status=args.status,
            review_status=args.review,
            note=args.note,
        )
        print(f"updated {n} link(s) for {args.card_name}")
        return 0
    if args.cmd == "fetch-images":
        n = themes.fetch_images_for_theme(
            args.slug, variant=args.variant, only_included=not args.all
        )
        print(f"fetched/recorded {n} image(s)")
        return 0
    if args.cmd == "packet":
        json_path, md_path = write_packet(args.slug)
        print(f"wrote {json_path}")
        print(f"wrote {md_path}")
        return 0
    return 1


def _dispatch_slides(args: argparse.Namespace) -> int:
    if args.cmd != "build":
        return 1
    out_path = Path(args.out) if args.out else None
    if args.backend == "v1":
        from .slideshow.v1_template.generator import build as build_v1
        path = build_v1(args.slug, out_path=out_path)
    else:
        from .slideshow.compiler.generator import build as build_compiler
        path = build_compiler(args.slug, out_path=out_path, style=args.style)
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
