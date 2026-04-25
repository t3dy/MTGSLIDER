from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
CACHE = ROOT / "cache"
SCRYFALL_CACHE = CACHE / "scryfall"
IMAGE_CACHE = CACHE / "images"
THEMES = ROOT / "themes"
DB_PATH = DATA / "mtgslider.sqlite"


def ensure_dirs() -> None:
    for p in (DATA, CACHE, SCRYFALL_CACHE, IMAGE_CACHE, THEMES):
        p.mkdir(parents=True, exist_ok=True)


def theme_dir(slug: str) -> Path:
    d = THEMES / slug
    (d / "images").mkdir(parents=True, exist_ok=True)
    (d / "out").mkdir(parents=True, exist_ok=True)
    return d
