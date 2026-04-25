-- MTGSLIDER schema. Themes-only (slice 1).

CREATE TABLE IF NOT EXISTS themes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    slug            TEXT NOT NULL UNIQUE,
    canonical_name  TEXT NOT NULL,
    short_description TEXT,
    research_status TEXT NOT NULL DEFAULT 'in_progress'
                    CHECK (research_status IN ('in_progress','ready_for_packet','ready_for_slides','archived')),
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS theme_aliases (
    theme_id INTEGER NOT NULL REFERENCES themes(id) ON DELETE CASCADE,
    alias    TEXT NOT NULL,
    PRIMARY KEY (theme_id, alias)
);

-- Cards are cached locally so theme review doesn't need Scryfall round-trips.
CREATE TABLE IF NOT EXISTS cards (
    scryfall_id     TEXT PRIMARY KEY,
    oracle_id       TEXT,
    name            TEXT NOT NULL,
    type_line       TEXT,
    mana_cost       TEXT,
    oracle_text     TEXT,
    colors          TEXT,           -- JSON array
    color_identity  TEXT,           -- JSON array
    legalities      TEXT,           -- JSON object
    set_code        TEXT,
    set_name        TEXT,
    rarity          TEXT,
    artist          TEXT,
    image_uris      TEXT,           -- JSON object
    scryfall_uri    TEXT,
    layout          TEXT,
    raw_json        TEXT NOT NULL,  -- full Scryfall payload for re-derivation
    fetched_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_cards_name ON cards(name);

-- A card can be linked to a theme for multiple reasons.
CREATE TABLE IF NOT EXISTS theme_card_links (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    theme_id        INTEGER NOT NULL REFERENCES themes(id) ON DELETE CASCADE,
    scryfall_id     TEXT NOT NULL REFERENCES cards(scryfall_id),
    link_type       TEXT NOT NULL
                    CHECK (link_type IN ('name_match','type_match','oracle_match','flavor_match','art_match','manual','scryfall_query')),
    link_reason     TEXT,
    confidence      REAL NOT NULL DEFAULT 0.5,
    include_status  TEXT NOT NULL DEFAULT 'uncertain'
                    CHECK (include_status IN ('include','exclude','uncertain','exemplar')),
    review_status   TEXT NOT NULL DEFAULT 'unreviewed'
                    CHECK (review_status IN ('unreviewed','reviewed')),
    note            TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    UNIQUE (theme_id, scryfall_id, link_type)
);

CREATE INDEX IF NOT EXISTS idx_links_theme ON theme_card_links(theme_id);

-- Image provenance lives here so it's queryable; physical files in themes/<slug>/images/.
CREATE TABLE IF NOT EXISTS theme_card_images (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    theme_id        INTEGER NOT NULL REFERENCES themes(id) ON DELETE CASCADE,
    scryfall_id     TEXT NOT NULL REFERENCES cards(scryfall_id),
    face_index      INTEGER NOT NULL DEFAULT 0,
    face_name       TEXT NOT NULL,
    variant         TEXT NOT NULL,
    source_url      TEXT NOT NULL,
    local_path      TEXT NOT NULL,
    downloaded_at   TEXT NOT NULL,
    UNIQUE (theme_id, scryfall_id, face_index, variant)
);

-- Historical-trip research cards (output of mtg-historical-trip skill).
-- Stored as both markdown on disk AND structured rows here so cross-queries are cheap.
CREATE TABLE IF NOT EXISTS historical_trips (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    slug            TEXT NOT NULL UNIQUE,           -- e.g. "scry", "conjure", "paracelsus", "rosicrucianism"
    source_type     TEXT NOT NULL
                    CHECK (source_type IN ('etymology','biography','tradition','database_concept')),
    title           TEXT NOT NULL,                  -- canonical name (the term, the person, the tradition)
    summary         TEXT NOT NULL,                  -- 1-2 sentence headline for tooltips and overlay panels
    body_markdown   TEXT NOT NULL,                  -- the full research card body
    source_path     TEXT NOT NULL,                  -- on-disk file the row was ingested from
    confidence      TEXT NOT NULL DEFAULT 'medium'
                    CHECK (confidence IN ('high','medium','low')),
    review_status   TEXT NOT NULL DEFAULT 'unreviewed'
                    CHECK (review_status IN ('unreviewed','reviewed','rejected')),
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_trips_source_type ON historical_trips(source_type);
CREATE INDEX IF NOT EXISTS idx_trips_review_status ON historical_trips(review_status);

-- Many-to-many: which historical trips reference which MTG cards (or themes).
CREATE TABLE IF NOT EXISTS trip_card_refs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id         INTEGER NOT NULL REFERENCES historical_trips(id) ON DELETE CASCADE,
    scryfall_id     TEXT REFERENCES cards(scryfall_id),
    theme_slug      TEXT,                           -- alternative anchor when no specific card
    relevance       TEXT NOT NULL DEFAULT 'medium' CHECK (relevance IN ('high','medium','low')),
    note            TEXT,
    UNIQUE (trip_id, scryfall_id, theme_slug)
);

-- Famous decks (Caw-Blade, Hogaak, Affinity, Storm, etc.) and their cards.
CREATE TABLE IF NOT EXISTS decklists (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    slug            TEXT NOT NULL UNIQUE,           -- e.g. "hogaak-bridgevine-mc-barcelona-2019"
    name            TEXT NOT NULL,                  -- "Hogaak Bridgevine"
    archetype       TEXT,                           -- "Hogaak Bridgevine" (often = name)
    format          TEXT NOT NULL,                  -- "Modern", "Standard", "Legacy", "Pioneer", etc.
    event_name      TEXT,                           -- "Mythic Championship IV Barcelona"
    event_date      TEXT,                           -- ISO date if known; partial otherwise
    placement       TEXT,                           -- "Top 8", "Won", "12-3", or NULL
    pilot           TEXT,                           -- player name if known
    source_url      TEXT,                           -- where the decklist was sourced
    notes_markdown  TEXT,                           -- commentary, banlist context, archetype notes
    review_status   TEXT NOT NULL DEFAULT 'reviewed' CHECK (review_status IN ('unreviewed','reviewed','rejected')),
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_decklists_format ON decklists(format);

CREATE TABLE IF NOT EXISTS decklist_cards (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    decklist_id     INTEGER NOT NULL REFERENCES decklists(id) ON DELETE CASCADE,
    scryfall_id     TEXT NOT NULL REFERENCES cards(scryfall_id),
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    location        TEXT NOT NULL CHECK (location IN ('mainboard','sideboard','commander','companion')),
    UNIQUE (decklist_id, scryfall_id, location)
);

CREATE INDEX IF NOT EXISTS idx_decklist_cards_deck ON decklist_cards(decklist_id);
CREATE INDEX IF NOT EXISTS idx_decklist_cards_card ON decklist_cards(scryfall_id);
