from conftest import load_ko_module


def test_join_matches_sqlite_result():
    m = load_ko_module("02-relational-model.py")
    users = m.Relation(("id", "name"), frozenset({(1, "Alice"), (2, "Bob")}))
    orders = m.Relation(
        ("id", "user_id", "product"), frozenset({(10, 1, "Bag"), (11, 2, "Hat")})
    )
    rel_out = users.join(orders, "id", "user_id").project(("name", "product"))
    sqlite_out = m.sqlite_join_result()
    assert sorted(rel_out.rows) == sorted(sqlite_out)
