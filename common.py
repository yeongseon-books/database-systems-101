from __future__ import annotations

import sqlite3
from collections import namedtuple
from pathlib import Path

Row = namedtuple("Row", ["id", "value"])


def make_db(path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def reset_file(path: str) -> None:
    p = Path(path)
    if p.exists():
        p.unlink()
