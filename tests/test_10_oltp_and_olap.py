from conftest import load_ko_module


def test_oltp_olap_and_column_aggregate_consistency():
    m = load_ko_module("10-oltp-and-olap.py")
    db = m.setup_orders(n=5000, seed=10)
    oltp_t = m.run_oltp_workload(db, iterations=200)
    olap_t, sql_rows = m.run_olap_workload(db)
    raw_rows = db.execute(
        "SELECT id, user_id, status, total, country FROM orders"
    ).fetchall()
    col_rows = m.column_store_aggregate(raw_rows)
    assert sorted(sql_rows) == sorted(col_rows)
    assert oltp_t >= 0.0 and olap_t >= 0.0
