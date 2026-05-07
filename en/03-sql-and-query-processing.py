"""Episode 03: SQL and query processing. Runnable example in English."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Query:
    columns: list[str]
    table: str
    where_col: str | None = None
    where_val: str | None = None
    order_by: str | None = None


def parse_sql(sql: str) -> Query:
    tokens = sql.strip().replace(",", " , ").split()
    s = tokens.index("SELECT")
    f = tokens.index("FROM")
    columns = [t for t in tokens[s + 1 : f] if t != ","]
    table = tokens[f + 1]
    where_col = where_val = order_by = None
    if "WHERE" in tokens:
        w = tokens.index("WHERE")
        where_col = tokens[w + 1]
        where_val = tokens[w + 3].strip("'\"")
    if "ORDER" in tokens:
        o = tokens.index("BY")
        order_by = tokens[o + 1]
    return Query(
        columns=columns,
        table=table,
        where_col=where_col,
        where_val=where_val,
        order_by=order_by,
    )


def execute_query(
    query: Query, tables: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    rows = list(tables[query.table])
    if query.where_col is not None:
        rows = [r for r in rows if str(r[query.where_col]) == str(query.where_val)]
    if query.order_by is not None:
        order_by = query.order_by
        rows.sort(key=lambda r: r[order_by])
    if query.columns != ["*"]:
        rows = [{c: r[c] for c in query.columns} for r in rows]
    return rows


if __name__ == "__main__":
    data = {
        "orders": [
            {"id": 2, "user_id": 7, "total": 50},
            {"id": 1, "user_id": 1, "total": 30},
        ]
    }
    q = parse_sql("SELECT id,total FROM orders WHERE user_id = '7' ORDER BY id")
    print(execute_query(q, data))
