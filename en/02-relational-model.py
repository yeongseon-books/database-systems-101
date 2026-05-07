"""Episode 02: Relational model. Runnable example in English."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True)
class Relation:
    schema: tuple[str, ...]
    rows: frozenset[tuple[object, ...]]

    def select(self, predicate):
        return Relation(
            self.schema,
            frozenset(r for r in self.rows if predicate(dict(zip(self.schema, r)))),
        )

    def project(self, columns: tuple[str, ...]):
        idx = [self.schema.index(c) for c in columns]
        return Relation(columns, frozenset(tuple(r[i] for i in idx) for r in self.rows))

    def union(self, other: "Relation"):
        assert self.schema == other.schema
        return Relation(self.schema, self.rows | other.rows)

    def difference(self, other: "Relation"):
        assert self.schema == other.schema
        return Relation(self.schema, self.rows - other.rows)

    def join(self, other: "Relation", left_key: str, right_key: str):
        li = self.schema.index(left_key)
        ri = other.schema.index(right_key)
        out_schema = self.schema + tuple(c for c in other.schema if c != right_key)
        out_rows = set()
        for l in self.rows:
            for r in other.rows:
                if l[li] == r[ri]:
                    out_rows.add(l + tuple(v for i, v in enumerate(r) if i != ri))
        return Relation(out_schema, frozenset(out_rows))


def sqlite_join_result() -> list[tuple[str, str]]:
    db = sqlite3.connect(":memory:")
    db.executescript(
        """
        CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE orders(id INTEGER PRIMARY KEY, user_id INTEGER, product TEXT);
        INSERT INTO users VALUES (1,'Alice'),(2,'Bob');
        INSERT INTO orders VALUES (10,1,'Bag'),(11,2,'Hat');
        """
    )
    return db.execute(
        "SELECT u.name, o.product FROM users u JOIN orders o ON u.id=o.user_id ORDER BY o.id"
    ).fetchall()


if __name__ == "__main__":
    users = Relation(("id", "name"), frozenset({(1, "Alice"), (2, "Bob")}))
    orders = Relation(
        ("id", "user_id", "product"), frozenset({(10, 1, "Bag"), (11, 2, "Hat")})
    )
    print(users.join(orders, "id", "user_id").project(("name", "product")))
