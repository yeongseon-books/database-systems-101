from conftest import load_ko_module


def test_parse_plan_execute_pipeline():
    m = load_ko_module("03-sql-and-query-processing.py")
    q = m.parse_sql("SELECT id,total FROM orders WHERE user_id = '7' ORDER BY id")
    data = {
        "orders": [
            {"id": 2, "user_id": 7, "total": 50},
            {"id": 1, "user_id": 7, "total": 30},
        ]
    }
    out = m.execute_query(q, data)
    assert out == [{"id": 1, "total": 30}, {"id": 2, "total": 50}]
