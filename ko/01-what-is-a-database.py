from __future__ import annotations

import json
import sqlite3
from pathlib import Path


def flat_file_deposit(path: Path, user_id: str, amount: int) -> None:
    data = json.loads(path.read_text()) if path.exists() else {}
    data[user_id] = data.get(user_id, 0) + amount
    path.write_text(json.dumps(data))


def sqlite_memory_demo() -> list[tuple[str, int]]:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE accounts(user_id TEXT PRIMARY KEY, balance INTEGER NOT NULL)"
    )
    conn.execute("INSERT INTO accounts VALUES (?, ?)", ("alice", 100))
    conn.execute(
        "UPDATE accounts SET balance = balance + 50 WHERE user_id = ?", ("alice",)
    )
    return conn.execute("SELECT user_id, balance FROM accounts").fetchall()


def sqlite_file_persistence_demo(path: Path) -> tuple[int, int]:
    with sqlite3.connect(path) as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS kv(k TEXT PRIMARY KEY, v INTEGER NOT NULL)"
        )
        db.execute(
            "INSERT OR REPLACE INTO kv VALUES ('counter', COALESCE((SELECT v FROM kv WHERE k='counter'),0)+1)"
        )
        first = db.execute("SELECT v FROM kv WHERE k='counter'").fetchone()[0]
    with sqlite3.connect(path) as db:
        second = db.execute("SELECT v FROM kv WHERE k='counter'").fetchone()[0]
    return first, second


if __name__ == "__main__":
    tmp_json = Path("tmp_ep01_accounts.json")
    tmp_db = Path("tmp_ep01.sqlite3")
    flat_file_deposit(tmp_json, "alice", 100)
    print("flat file:", json.loads(tmp_json.read_text()))
    print("sqlite memory:", sqlite_memory_demo())
    print("sqlite file persistence:", sqlite_file_persistence_demo(tmp_db))
