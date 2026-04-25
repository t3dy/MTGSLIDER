from tests.conftest import make_card, make_dfc


def test_named_returns_normalized_card(mock_scryfall):
    from mtgslider import scryfall

    raw = make_card("Counterspell")
    mock_scryfall.named[("counterspell", False)] = raw

    card = scryfall.named("Counterspell")
    assert card is not None
    assert card.name == "Counterspell"
    assert card.colors == ["U"]
    assert card.image_uris["normal"] == "https://img.test/normal.jpg"
    assert card.faces == []


def test_named_returns_none_on_404(mock_scryfall):
    from mtgslider import scryfall
    assert scryfall.named("Nonexistent Card") is None


def test_double_faced_card_has_faces(mock_scryfall):
    from mtgslider import scryfall

    raw = make_dfc("Delver of Secrets", "Insectile Aberration")
    mock_scryfall.named[("delver of secrets", False)] = raw

    card = scryfall.named("Delver of Secrets")
    assert card is not None
    assert len(card.faces) == 2
    assert card.faces[0].name == "Delver of Secrets"
    assert card.faces[1].name == "Insectile Aberration"
    # parent image_uris should be inherited from front face
    assert card.image_uris.get("normal") == "https://img.test/front.jpg"


def test_search_paginates(mock_scryfall):
    from mtgslider import scryfall

    mock_scryfall.searches["t:wizard"] = [make_card("Snapcaster Mage"), make_card("Baral, Chief of Compliance")]
    results = list(scryfall.search("t:wizard"))
    assert [c.name for c in results] == ["Snapcaster Mage", "Baral, Chief of Compliance"]
