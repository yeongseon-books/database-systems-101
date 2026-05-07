"""Episode 10: OLTP and OLAP. Runnable example in English."""
from __future__ import annotations

import random
import sqlite3
import time
from collections import defaultdict


def setup_orders(n: int = 20_000, seed: int = 123) -> sqlite3.Connection:
    random.seed(seed)
    db = sqlite3.connect(":memory:")
    db.executescript(
        """
        CREATE TABLE orders(
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            status TEXT,
            total INTEGER,
            country TEXT
        );
        CREATE INDEX idx_orders_user_id ON orders(user_id);
        """
    )
    rows = [
        (
            i,
            random.randint(1, 2000),
            random.choice(["paid", "pending", "cancelled"]),
            random.randint(10, 1000),
            random.choice(["KR", "US", "JP"]),
        )
        for i in range(1, n + 1)
    ]
    db.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
    return db


def run_oltp_workload(db: sqlite3.Connection, iterations: int = 500) -> float:
    start = time.perf_counter()
    for i in range(iterations):
        user_id = (i % 2000) + 1
        db.execute(
            "SELECT total FROM orders WHERE user_id = ? LIMIT 1", (user_id,)
        ).fetchone()
    return time.perf_counter() - start


def run_olap_workload(db: sqlite3.Connection) -> tuple[float, list[tuple[str, int]]]:
    start = time.perf_counter()
    rows = db.execute(
        "SELECT country, SUM(total) FROM orders WHERE status='paid' GROUP BY country ORDER BY country"
    ).fetchall()
    return time.perf_counter() - start, rows


def column_store_aggregate(
    rows: list[tuple[int, int, str, int, str]],
) -> list[tuple[str, int]]:
    status = [r[2] for r in rows]
    total = [r[3] for r in rows]
    country = [r[4] for r in rows]
    agg: dict[str, int] = defaultdict(int)
    for i in range(len(rows)):
        if status[i] == "paid":
            agg[country[i]] += total[i]
    return sorted(agg.items())


if __name__ == "__main__":
    db = setup_orders()
    print("oltp sec:", run_oltp_workload(db))
    print("olap sec:", run_olap_workload(db)[0])
