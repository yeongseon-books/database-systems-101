"""Episode 05: Transactions and ACID. Runnable example in English."""
from __future__ import annotations

import sqlite3
from pathlib import Path


def init_bank(db_path: Path) -> None:
    with sqlite3.connect(db_path) as db:
        db.executescript(
            """
            DROP TABLE IF EXISTS accounts;
            CREATE TABLE accounts(id INTEGER PRIMARY KEY, owner TEXT, balance INTEGER NOT NULL CHECK(balance >= 0));
            INSERT INTO accounts VALUES (1,'Alice',1000),(2,'Bob',1000);
            """
        )


def transfer(
    db_path: Path, src: int, dst: int, amount: int, fail_midway: bool = False
) -> None:
    with sqlite3.connect(db_path) as db:
        try:
            db.execute("BEGIN")
            db.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, src)
            )
            if fail_midway:
                raise RuntimeError("simulated failure")
            db.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, dst)
            )
            db.execute("COMMIT")
        except Exception:
            db.execute("ROLLBACK")
            raise


class ToyWAL:
    def __init__(self):
        self.state = {"Alice": 1000, "Bob": 1000}
        self.log: list[tuple[str, str, int]] = []

    def append_transfer(self, src: str, dst: str, amount: int) -> None:
        self.log.append((src, dst, amount))

    def apply(self) -> None:
        for src, dst, amount in self.log:
            self.state[src] -= amount
            self.state[dst] += amount


def balances(db_path: Path) -> dict[str, int]:
    with sqlite3.connect(db_path) as db:
        return {
            owner: bal
            for owner, bal in db.execute(
                "SELECT owner, balance FROM accounts ORDER BY id"
            )
        }


if __name__ == "__main__":
    p = Path("tmp_ep05.db")
    init_bank(p)
    transfer(p, 1, 2, 100)
    print(balances(p))
