"""Scryfall API client. Cached on disk, rate-limited per Scryfall guidelines.

Scryfall asks for >=50ms between requests and a meaningful User-Agent.
https://scryfall.com/docs/api
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional
from urllib.parse import urlencode

import requests

from . import __version__
from .paths import SCRYFALL_CACHE, ensure_dirs

USER_AGENT = f"mtgslider/{__version__} (research tool; contact: local)"
ACCEPT = "application/json;q=0.9,*/*;q=0.8"
BASE = "https://api.scryfall.com"
MIN_INTERVAL_S = 0.1  # 100ms — comfortably above Scryfall's 50ms ask


_last_request_at = 0.0


def _rate_limit() -> None:
    global _last_request_at
    now = time.monotonic()
    delta = now - _last_request_at
    if delta < MIN_INTERVAL_S:
        time.sleep(MIN_INTERVAL_S - delta)
    _last_request_at = time.monotonic()


def _cache_path(url: str, params: Optional[dict] = None) -> Path:
    key_src = url + (("?" + urlencode(sorted(params.items()))) if params else "")
    h = hashlib.sha256(key_src.encode("utf-8")).hexdigest()[:32]
    return SCRYFALL_CACHE / f"{h}.json"


def _get(path: str, params: Optional[dict] = None, *, use_cache: bool = True) -> dict:
    ensure_dirs()
    url = path if path.startswith("http") else f"{BASE}{path}"
    cache_file = _cache_path(url, params)
    if use_cache and cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))

    _rate_limit()
    resp = requests.get(
        url,
        params=params,
        headers={"User-Agent": USER_AGENT, "Accept": ACCEPT},
        timeout=30,
    )
    if resp.status_code == 404:
        # Cache 404s so a typo doesn't repeatedly hit the API.
        body = {"object": "error", "status": 404, "details": "Not found"}
        cache_file.write_text(json.dumps(body), encoding="utf-8")
        return body
    resp.raise_for_status()
    body = resp.json()
    cache_file.write_text(json.dumps(body), encoding="utf-8")
    return body


@dataclass
class Card:
    """Normalized Scryfall card. Handles double-faced layouts."""
    id: str
    oracle_id: str
    name: str
    mana_cost: str
    type_line: str
    oracle_text: str
    colors: list[str]
    color_identity: list[str]
    legalities: dict[str, str]
    set_code: str
    set_name: str
    collector_number: str
    rarity: str
    artist: str
    image_uris: dict[str, str]
    prices: dict[str, Optional[str]]
    scryfall_uri: str
    layout: str
    faces: list["Card"] = field(default_factory=list)

    @classmethod
    def from_scryfall(cls, raw: dict) -> "Card":
        # Double-faced cards put image_uris under each face, not the parent.
        image_uris = raw.get("image_uris", {}) or {}
        faces: list[Card] = []
        if not image_uris and raw.get("card_faces"):
            for face_raw in raw["card_faces"]:
                face = cls(
                    id=raw["id"],  # share parent id
                    oracle_id=raw.get("oracle_id", ""),
                    name=face_raw.get("name", ""),
                    mana_cost=face_raw.get("mana_cost", ""),
                    type_line=face_raw.get("type_line", ""),
                    oracle_text=face_raw.get("oracle_text", ""),
                    colors=face_raw.get("colors", raw.get("colors", [])),
                    color_identity=raw.get("color_identity", []),
                    legalities=raw.get("legalities", {}),
                    set_code=raw.get("set", ""),
                    set_name=raw.get("set_name", ""),
                    collector_number=raw.get("collector_number", ""),
                    rarity=raw.get("rarity", ""),
                    artist=face_raw.get("artist", raw.get("artist", "")),
                    image_uris=face_raw.get("image_uris", {}) or {},
                    prices=raw.get("prices", {}),
                    scryfall_uri=raw.get("scryfall_uri", ""),
                    layout=raw.get("layout", ""),
                )
                faces.append(face)
            # Use first face's images as the card's primary
            if faces and faces[0].image_uris:
                image_uris = faces[0].image_uris

        return cls(
            id=raw["id"],
            oracle_id=raw.get("oracle_id", ""),
            name=raw.get("name", ""),
            mana_cost=raw.get("mana_cost", ""),
            type_line=raw.get("type_line", ""),
            oracle_text=raw.get("oracle_text", ""),
            colors=raw.get("colors", []),
            color_identity=raw.get("color_identity", []),
            legalities=raw.get("legalities", {}),
            set_code=raw.get("set", ""),
            set_name=raw.get("set_name", ""),
            collector_number=raw.get("collector_number", ""),
            rarity=raw.get("rarity", ""),
            artist=raw.get("artist", ""),
            image_uris=image_uris,
            prices=raw.get("prices", {}),
            scryfall_uri=raw.get("scryfall_uri", ""),
            layout=raw.get("layout", ""),
            faces=faces,
        )

    def to_dict(self) -> dict:
        d = {k: v for k, v in self.__dict__.items() if k != "faces"}
        d["faces"] = [f.to_dict() for f in self.faces]
        return d


def named(name: str, *, fuzzy: bool = False) -> Optional[Card]:
    """Exact (or fuzzy) lookup by card name. Returns None on 404."""
    params = {"fuzzy" if fuzzy else "exact": name}
    body = _get("/cards/named", params=params)
    if body.get("object") == "error":
        return None
    return Card.from_scryfall(body)


def by_id(scryfall_id: str) -> Optional[Card]:
    body = _get(f"/cards/{scryfall_id}")
    if body.get("object") == "error":
        return None
    return Card.from_scryfall(body)


def search(query: str, *, unique: str = "cards", order: str = "name") -> Iterator[Card]:
    """Paginated search using Scryfall syntax (e.g. 't:creature o:zombie')."""
    params = {"q": query, "unique": unique, "order": order}
    next_url: Optional[str] = "/cards/search"
    while next_url:
        body = _get(next_url, params=params if next_url == "/cards/search" else None)
        if body.get("object") == "error":
            # 404 on search means "no cards found" — return without yielding.
            return
        for raw in body.get("data", []):
            yield Card.from_scryfall(raw)
        if body.get("has_more"):
            next_url = body.get("next_page")
            params = None
        else:
            next_url = None


def search_list(query: str, *, limit: Optional[int] = None) -> list[Card]:
    out: list[Card] = []
    for card in search(query):
        out.append(card)
        if limit is not None and len(out) >= limit:
            break
    return out


def collection(identifiers: Iterable[dict]) -> list[Card]:
    """Bulk lookup via /cards/collection. Identifiers per Scryfall spec."""
    ids = list(identifiers)
    if not ids:
        return []
    out: list[Card] = []
    # Scryfall caps at 75 per request
    for i in range(0, len(ids), 75):
        chunk = ids[i : i + 75]
        ensure_dirs()
        _rate_limit()
        resp = requests.post(
            f"{BASE}/cards/collection",
            json={"identifiers": chunk},
            headers={"User-Agent": USER_AGENT, "Accept": ACCEPT, "Content-Type": "application/json"},
            timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()
        for raw in body.get("data", []):
            out.append(Card.from_scryfall(raw))
    return out
