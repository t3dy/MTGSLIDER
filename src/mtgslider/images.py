"""Card image downloader. Records provenance, dedupes by Scryfall ID + variant."""
from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

import requests

from . import __version__
from .paths import IMAGE_CACHE, ensure_dirs
from .scryfall import Card, MIN_INTERVAL_S

VARIANTS = ("small", "normal", "large", "png", "art_crop", "border_crop")
DEFAULT_VARIANT = "normal"

_USER_AGENT = f"mtgslider/{__version__}"


@dataclass
class ImageRecord:
    scryfall_id: str
    card_name: str
    face_index: int
    face_name: str
    variant: str
    source_url: str
    local_path: Path
    downloaded_at: str  # ISO8601 UTC

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        d["local_path"] = str(self.local_path)
        return d


def _ext_for(variant: str) -> str:
    return "png" if variant == "png" else "jpg"


def _filename(card: Card, face_index: int, variant: str) -> str:
    # Deterministic — re-runs land on the same path.
    base = f"{card.id}_{face_index}_{variant}"
    return f"{base}.{_ext_for(variant)}"


def _faces_for(card: Card) -> list[tuple[int, str, dict]]:
    """Return [(face_index, face_name, image_uris), ...]."""
    if card.faces:
        return [(i, f.name, f.image_uris) for i, f in enumerate(card.faces)]
    return [(0, card.name, card.image_uris)]


_last_download_at = 0.0


def _rate_limit() -> None:
    # Scryfall image CDN is more permissive than the API but still be polite.
    global _last_download_at
    now = time.monotonic()
    delta = now - _last_download_at
    if delta < MIN_INTERVAL_S:
        time.sleep(MIN_INTERVAL_S - delta)
    _last_download_at = time.monotonic()


def fetch_card_images(
    card: Card,
    variant: str = DEFAULT_VARIANT,
    *,
    out_dir: Optional[Path] = None,
) -> list[ImageRecord]:
    if variant not in VARIANTS:
        raise ValueError(f"variant must be one of {VARIANTS!r}, got {variant!r}")
    ensure_dirs()
    target_dir = out_dir or IMAGE_CACHE
    target_dir.mkdir(parents=True, exist_ok=True)

    records: list[ImageRecord] = []
    for face_index, face_name, image_uris in _faces_for(card):
        url = image_uris.get(variant)
        if not url:
            continue
        local_path = target_dir / _filename(card, face_index, variant)
        if not local_path.exists():
            _rate_limit()
            resp = requests.get(url, headers={"User-Agent": _USER_AGENT}, timeout=60)
            resp.raise_for_status()
            local_path.write_bytes(resp.content)
        records.append(
            ImageRecord(
                scryfall_id=card.id,
                card_name=card.name,
                face_index=face_index,
                face_name=face_name,
                variant=variant,
                source_url=url,
                local_path=local_path,
                downloaded_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            )
        )
    return records


def fetch_many(
    cards: Iterable[Card],
    variant: str = DEFAULT_VARIANT,
    *,
    out_dir: Optional[Path] = None,
) -> list[ImageRecord]:
    all_records: list[ImageRecord] = []
    for card in cards:
        all_records.extend(fetch_card_images(card, variant, out_dir=out_dir))
    return all_records
