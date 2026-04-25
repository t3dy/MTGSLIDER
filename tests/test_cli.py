"""Smoke-test the CLI dispatcher end-to-end (sans network)."""
from tests.conftest import make_card


def test_cli_create_and_packet(mock_scryfall, mock_image_downloader, capsys):
    from mtgslider.cli import main

    mock_scryfall.searches["t:wizard"] = [make_card("Snapcaster Mage")]

    assert main(["theme", "create", "Wizards"]) == 0
    assert main(["theme", "find-cards", "wizards", "--query", "t:wizard"]) == 0
    assert main(["theme", "mark", "wizards", "Snapcaster Mage", "--status", "include"]) == 0
    assert main(["theme", "fetch-images", "wizards"]) == 0
    assert main(["theme", "packet", "wizards"]) == 0
    out = capsys.readouterr().out
    assert "packet.json" in out


def test_cli_slides_v1(mock_scryfall, mock_image_downloader):
    from mtgslider.cli import main

    mock_scryfall.searches["t:wizard"] = [make_card("Snapcaster Mage")]
    main(["theme", "create", "Wizards"])
    main(["theme", "find-cards", "wizards", "--query", "t:wizard"])
    main(["theme", "mark", "wizards", "Snapcaster Mage", "--status", "include"])
    main(["theme", "fetch-images", "wizards"])

    assert main(["slides", "build", "wizards", "--backend", "v1"]) == 0


def test_cli_slides_compiler(mock_scryfall, mock_image_downloader):
    from mtgslider.cli import main

    mock_scryfall.searches["t:wizard"] = [make_card("Snapcaster Mage")]
    main(["theme", "create", "Wizards"])
    main(["theme", "find-cards", "wizards", "--query", "t:wizard"])
    main(["theme", "mark", "wizards", "Snapcaster Mage", "--status", "exemplar"])
    main(["theme", "fetch-images", "wizards"])

    assert main(["slides", "build", "wizards", "--backend", "compiler", "--style", "rhystic"]) == 0
