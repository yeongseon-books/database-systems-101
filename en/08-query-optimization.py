"""Episode 08: Query optimization. Runnable example in English."""
from __future__ import annotations

import random
import time


def estimate_join_cost(
    left_rows: int, right_rows: int, method: str = "nested_loop"
) -> int:
    if method == "nested_loop":
        return left_rows * right_rows
    if method == "hash_join":
        return left_rows + right_rows
    raise ValueError("unknown method")


def estimate_plan_cost(stats: dict[str, int], plan: tuple[str, str, str]) -> int:
    a, b, c = plan
    ab = estimate_join_cost(stats[a], stats[b], "hash_join")
    ab_rows = max(1, min(stats[a], stats[b]) // 10)
    abc = estimate_join_cost(ab_rows, stats[c], "hash_join")
    return ab + abc


def pick_best_plan(stats: dict[str, int]) -> tuple[tuple[str, str, str], int]:
    plans = (("A", "B", "C"), ("A", "C", "B"))
    scored = [(p, estimate_plan_cost(stats, p)) for p in plans]
    return min(scored, key=lambda x: x[1])


def run_join_simulation(
    plan: tuple[str, str, str], stats: dict[str, int], seed: int = 0
) -> float:
    random.seed(seed)
    start = time.perf_counter()
    n = estimate_plan_cost(stats, plan) // 20
    acc = 0
    for i in range(n):
        acc += (i * 7) % 13
    return time.perf_counter() - start + (acc * 0.0)


if __name__ == "__main__":
    s = {"A": 1000, "B": 100, "C": 5000}
    print(pick_best_plan(s))
