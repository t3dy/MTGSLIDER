"""Shared test fixtures. Redirects all on-disk state into a tmp dir per test."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture(autouse=True)
def isolated_paths(tmp_path, monkeypatch):
    """Redirect data, cache, themes, and DB into a per-test tmp dir."""
    from mtgslider import paths as paths_mod

    new_root = tmp_path
    new_data = new_root / "data"
    new_cache = new_root / "cache"
    new_scry = new_cache / "scryfall"
    new_imgs = new_cache / "images"
    new_themes = new_root / "themes"
    new_db = new_data / "mtgslider.sqlite"

    monkeypatch.setattr(paths_mod, "ROOT", new_root)
    monkeypatch.setattr(paths_mod, "DATA", new_data)
    monkeypatch.setattr(paths_mod, "CACHE", new_cache)
    monkeypatch.setattr(paths_mod, "SCRYFALL_CACHE", new_scry)
    monkeypatch.setattr(paths_mod, "IMAGE_CACHE", new_imgs)
    monkeypatch.setattr(paths_mod, "THEMES", new_themes)
    monkeypatch.setattr(paths_mod, "DB_PATH", new_db)

    # Re-route consumers that captured these at import time.
    from mtgslider import scryfall as scry_mod
    monkeypatch.setattr(scry_mod, "SCRYFALL_CACHE", new_scry)
    from mtgslider import images as img_mod
    monkeypatch.setattr(img_mod, "IMAGE_CACHE", new_imgs)
    from mtgslider import db as db_mod
    monkeypatch.setattr(db_mod, "DB_PATH", new_db)

    yield new_root


@pytest.fixture
def mock_scryfall(monkeypatch):
    """Replace the network layer with deterministic in-memory responses."""
    from mtgslider import scryfall as s

    class _Store:
        named: dict[tuple[str, bool], dict] = {}
        searches: dict[str, list[dict]] = {}

    store = _Store()

    def fake_get(path, params=None, *, use_cache=True):
        if path == "/cards/named":
            params = params or {}
            name = params.get("exact") or params.get("fuzzy")
            fuzzy = "fuzzy" in params
            key = (name.lower(), fuzzy)
            if key in store.named:
                return store.named[key]
            return {"object": "error", "status": 404, "details": "not found"}
        if path == "/cards/search":
            params = params or {}
            q = params.get("q", "")
            results = store.searches.get(q, [])
            return {"object": "list", "data": results, "has_more": False}
        if path.startswith("/cards/"):
            scry_id = path.split("/")[-1]
            for resp in store.named.values():
                if resp.get("id") == scry_id:
                    return resp
            return {"object": "error", "status": 404, "details": "not found"}
        return {"object": "error", "status": 404, "details": "not found"}

    monkeypatch.setattr(s, "_get", fake_get)
    return store


@pytest.fixture
def mock_image_downloader(monkeypatch, tmp_path):
    """Replace requests.get inside images.py with a fake that writes a 1x1 PNG."""
    from mtgslider import images as img_mod
    PNG_1x1 = bytes.fromhex(
        "89504E470D0A1A0A0000000D49484452000000010000000108060000001F15C4"
        "890000000A49444154789C636000000002000148AFA4710000000049454E44AE426082"
    )

    class FakeResp:
        def __init__(self):
            self.content = PNG_1x1
            self.status_code = 200
        def raise_for_status(self):
            pass

    def fake_get(url, **kwargs):
        return FakeResp()

    monkeypatch.setattr(img_mod.requests, "get", fake_get)
    return PNG_1x1


def make_card(name: str, **overrides) -> dict:
    """Build a Scryfall-shaped card payload for tests."""
    base = {
        "object": "card",
        "id": f"id-{name.lower().replace(' ', '-')}",
        "oracle_id": f"oid-{name.lower().replace(' ', '-')}",
        "name": name,
        "mana_cost": "{2}{U}",
        "type_line": "Creature — Wizard",
        "oracle_text": "Sample text.",
        "colors": ["U"],
        "color_identity": ["U"],
        "legalities": {"commander": "legal", "modern": "legal"},
        "set": "tst",
        "set_name": "Test Set",
        "collector_number": "1",
        "rarity": "rare",
        "artist": "Test Artist",
        "image_uris": {
            "small": "https://img.test/small.jpg",
            "normal": "https://img.test/normal.jpg",
            "large": "https://img.test/large.jpg",
            "png": "https://img.test/card.png",
            "art_crop": "https://img.test/art.jpg",
            "border_crop": "https://img.test/border.jpg",
        },
        "prices": {"usd": "1.00"},
        "scryfall_uri": "https://scryfall.com/c/test",
        "layout": "normal",
    }
    base.update(overrides)
    return base


def make_dfc(front_name: str, back_name: str, **overrides) -> dict:
    """Build a double-faced card payload."""
    base = {
        "object": "card",
        "id": f"id-{front_name.lower().replace(' ', '-')}-dfc",
        "oracle_id": f"oid-{front_name.lower().replace(' ', '-')}-dfc",
        "name": f"{front_name} // {back_name}",
        "type_line": "Creature — Werewolf // Creature — Werewolf",
        "colors": ["R"],
        "color_identity": ["R"],
        "legalities": {"modern": "legal"},
        "set": "tst", "set_name": "Test Set", "collector_number": "2",
        "rarity": "mythic", "artist": "Test Artist",
        "prices": {"usd": "5.00"},
        "scryfall_uri": "https://scryfall.com/c/dfc",
        "layout": "transform",
        "card_faces": [
            {
                "name": front_name,
                "mana_cost": "{2}{R}",
                "type_line": "Creature — Werewolf",
                "oracle_text": "Front text.",
                "colors": ["R"],
                "image_uris": {
                    "normal": "https://img.test/front.jpg",
                    "large": "https://img.test/front.large.jpg",
                },
            },
            {
                "name": back_name,
                "mana_cost": "",
                "type_line": "Creature — Werewolf",
                "oracle_text": "Back text.",
                "colors": ["R"],
                "image_uris": {
                    "normal": "https://img.test/back.jpg",
                    "large": "https://img.test/back.large.jpg",
                },
            },
        ],
    }
    base.update(overrides)
    return base
