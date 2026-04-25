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
