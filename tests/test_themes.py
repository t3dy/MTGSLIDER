from tests.conftest import make_card, make_dfc


def test_create_and_list_theme():
    from mtgslider import themes

    t = themes.create_theme("Alchemists", short_description="People who do alchemy", aliases=["mages of matter"])
    assert t["slug"] == "alchemists"
    assert t["aliases"] == ["mages of matter"]
    listed = themes.list_themes()
    assert any(x["slug"] == "alchemists" for x in listed)


def test_find_cards_by_query_stages_uncertain(mock_scryfall):
    from mtgslider import themes

    themes.create_theme("Wizards")
    mock_scryfall.searches["t:wizard"] = [make_card("Snapcaster Mage"), make_card("Baral, Chief of Compliance")]

    n = themes.find_cards_by_query("wizards", "t:wizard")
    assert n == 2
    links = themes.list_links("wizards")
    assert len(links) == 2
    assert all(l["include_status"] == "uncertain" for l in links)


def test_mark_card_changes_status(mock_scryfall):
    from mtgslider import themes

    themes.create_theme("Wizards")
    mock_scryfall.searches["t:wizard"] = [make_card("Snapcaster Mage")]
    themes.find_cards_by_query("wizards", "t:wizard")

    themes.mark_card("wizards", "Snapcaster Mage", include_status="exemplar", review_status="reviewed", note="defines tempo")
    [link] = themes.list_links("wizards")
    assert link["include_status"] == "exemplar"
    assert link["review_status"] == "reviewed"
    assert link["note"] == "defines tempo"


def test_add_card_by_name_uses_fuzzy(mock_scryfall):
    from mtgslider import themes

    themes.create_theme("Counterspells")
    mock_scryfall.named[("countrspell", True)] = make_card("Counterspell")

    card = themes.add_card_by_name("counterspells", "Countrspell", fuzzy=True)
    assert card is not None
    assert card.name == "Counterspell"
    [link] = themes.list_links("counterspells")
    assert link["include_status"] == "include"


def test_dfc_round_trips_through_cache(mock_scryfall):
    from mtgslider import themes

    themes.create_theme("Werewolves")
    mock_scryfall.searches["t:werewolf"] = [make_dfc("Delver of Secrets", "Insectile Aberration")]
    themes.find_cards_by_query("werewolves", "t:werewolf")

    # Now hit the cache path through fetch_images_for_theme's get_cached_card.
    from mtgslider.db import connect
    from mtgslider.themes import get_cached_card
    with connect() as conn:
        rows = conn.execute("SELECT scryfall_id FROM cards").fetchall()
        assert len(rows) == 1
        card = get_cached_card(rows[0]["scryfall_id"], conn=conn)
    assert card is not None
    assert len(card.faces) == 2
    assert card.faces[0].name == "Delver of Secrets"


def test_fetch_images_writes_files_and_records(mock_scryfall, mock_image_downloader):
    from mtgslider import themes
    from mtgslider.paths import theme_dir

    themes.create_theme("Wizards")
    mock_scryfall.searches["t:wizard"] = [make_card("Snapcaster Mage")]
    themes.find_cards_by_query("wizards", "t:wizard")
    themes.mark_card("wizards", "Snapcaster Mage", include_status="include")

    n = themes.fetch_images_for_theme("wizards", variant="normal")
    assert n == 1
    files = list((theme_dir("wizards") / "images").glob("*.jpg"))
    assert len(files) == 1

    images = themes.list_images("wizards")
    assert len(images) == 1
    assert images[0]["variant"] == "normal"
    assert images[0]["source_url"] == "https://img.test/normal.jpg"


def test_fetch_images_dfc_writes_both_faces(mock_scryfall, mock_image_downloader):
    from mtgslider import themes
    from mtgslider.paths import theme_dir

    themes.create_theme("Werewolves")
    mock_scryfall.searches["t:werewolf"] = [make_dfc("Delver of Secrets", "Insectile Aberration")]
    themes.find_cards_by_query("werewolves", "t:werewolf")
    themes.mark_card("werewolves", "Delver of Secrets // Insectile Aberration", include_status="include")

    n = themes.fetch_images_for_theme("werewolves", variant="normal")
    assert n == 2
    files = sorted((theme_dir("werewolves") / "images").glob("*.jpg"))
    assert len(files) == 2
