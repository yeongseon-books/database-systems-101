from conftest import load_ko_module


def test_optimizer_picks_lower_estimated_cost_plan():
    m = load_ko_module("08-query-optimization.py")
    stats = {"A": 1000, "B": 100, "C": 5000}
    best_plan, best_cost = m.pick_best_plan(stats)
    alt = ("A", "C", "B") if best_plan == ("A", "B", "C") else ("A", "B", "C")
    assert best_cost < m.estimate_plan_cost(stats, alt)
