from pathlib import Path
from tests.conftest import make_card


def _seed(mock_scryfall, mock_image_downloader):
    from mtgslider import themes
    themes.create_theme(
        "Books", short_description="Cards depicting books, scrolls, and writing.", aliases=["scrolls", "tomes"],
    )
    mock_scryfall.searches["o:book"] = [
        make_card("Library of Alexandria"),
        make_card("Jace's Archivist"),
        make_card("Whispering Madness"),
    ]
    themes.find_cards_by_query("books", "o:book")
    themes.mark_card("books", "Library of Alexandria", include_status="exemplar")
    themes.mark_card("books", "Jace's Archivist", include_status="include")
    # Whispering Madness left as uncertain.
    themes.fetch_images_for_theme("books", variant="normal")


def test_packet_buckets_and_writes_files(mock_scryfall, mock_image_downloader, tmp_path):
    _seed(mock_scryfall, mock_image_downloader)
    from mtgslider.packet import build_packet, write_packet

    packet = build_packet("books")
    assert packet["theme"]["slug"] == "books"
    assert packet["counts"]["exemplar"] == 1
    assert packet["counts"]["include"] == 1
    assert packet["counts"]["uncertain"] == 1
    assert packet["counts"]["with_images"] == 2  # exemplar + include have images

    json_path, md_path = write_packet("books")
    assert json_path.exists()
    assert md_path.exists()
    md = md_path.read_text(encoding="utf-8")
    assert "Library of Alexandria" in md


def test_v1_slideshow_builds(mock_scryfall, mock_image_downloader):
    _seed(mock_scryfall, mock_image_downloader)
    from mtgslider.slideshow.v1_template.generator import build

    out = build("books")
    assert out.exists()
    assert out.suffix == ".pptx"
    assert out.stat().st_size > 1000  # not an empty file


def test_compiler_slideshow_builds_default(mock_scryfall, mock_image_downloader):
    _seed(mock_scryfall, mock_image_downloader)
    from mtgslider.slideshow.compiler.generator import build

    out = build("books")
    assert out.exists()
    assert out.suffix == ".pptx"


def test_compiler_slideshow_builds_each_preset(mock_scryfall, mock_image_downloader):
    _seed(mock_scryfall, mock_image_downloader)
    from mtgslider.slideshow.compiler.generator import build

    paths = []
    for style in ("rhystic", "sierkovitz", "teaching"):
        paths.append(build("books", style=style))
    # All three produce distinct output files.
    assert len({p.name for p in paths}) == 3
    for p in paths:
        assert p.exists()


def test_compiler_validates_units(mock_scryfall, mock_image_downloader):
    """If the planner hands back a malformed unit, the generator must refuse."""
    from mtgslider.slideshow.compiler.slide_types import ArgumentUnit, validate_units

    bad = ArgumentUnit(slide_type="thesis", rhetorical_role="framing", content={})
    errors = validate_units([bad])
    assert errors  # missing 'title' and 'claim'


def test_compiler_unknown_preset_raises():
    from mtgslider.slideshow.compiler.presets import resolve
    import pytest
    with pytest.raises(ValueError):
        resolve("not-a-real-preset")
