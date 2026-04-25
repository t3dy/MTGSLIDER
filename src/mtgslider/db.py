"""SQLite connection + migration helper."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from .paths import DB_PATH, ensure_dirs

_SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def connect(db_path: Optional[Path] = None) -> sqlite3.Connection:
    ensure_dirs()
    target = db_path or DB_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    _migrate(conn)
    return conn


def _migrate(conn: sqlite3.Connection) -> None:
    sql = _SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(sql)
    conn.commit()
