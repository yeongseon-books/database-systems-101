"""Episode 04: Indexes. Runnable example in English."""

from __future__ import annotations

import random
import time


class BSTNode:
    def __init__(self, key: int, row: dict[str, int]):
        self.key = key
        self.rows = [row]
        self.left: BSTNode | None = None
        self.right: BSTNode | None = None


class BSTIndex:
    def __init__(self):
        self.root = None

    def insert(self, key: int, row: dict[str, int]) -> None:
        if self.root is None:
            self.root = BSTNode(key, row)
            return
        cur = self.root
        while True:
            if key == cur.key:
                cur.rows.append(row)
                return
            if key < cur.key:
                if cur.left is None:
                    cur.left = BSTNode(key, row)
                    return
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = BSTNode(key, row)
                    return
                cur = cur.right

    def lookup(self, key: int) -> tuple[list[dict[str, int]], int]:
        cur = self.root
        steps = 0
        while cur is not None:
            steps += 1
            if key == cur.key:
                return cur.rows, steps
            cur = cur.left if key < cur.key else cur.right
        return [], steps


class HashIndex:
    def __init__(self):
        self.store: dict[int, list[dict[str, int]]] = {}

    def insert(self, key: int, row: dict[str, int]) -> None:
        self.store.setdefault(key, []).append(row)

    def lookup(self, key: int) -> tuple[list[dict[str, int]], int]:
        return self.store.get(key, []), 1


def full_scan(
    rows: list[dict[str, int]], target: int
) -> tuple[list[dict[str, int]], int]:
    out = []
    steps = 0
    for r in rows:
        steps += 1
        if r["user_id"] == target:
            out.append(r)
    return out, steps


def benchmark_lookup(n: int = 10_000, seed: int = 42) -> dict[str, float | int]:
    random.seed(seed)
    rows = [{"id": i, "user_id": random.randint(1, 1000), "v": i * 3} for i in range(n)]
    target = rows[n // 2]["user_id"]
    bst = BSTIndex()
    hidx = HashIndex()
    for r in rows:
        bst.insert(r["user_id"], r)
        hidx.insert(r["user_id"], r)
    t0 = time.perf_counter()
    _, scan_steps = full_scan(rows, target)
    scan_t = time.perf_counter() - t0
    t1 = time.perf_counter()
    _, bst_steps = bst.lookup(target)
    bst_t = time.perf_counter() - t1
    t2 = time.perf_counter()
    _, hash_steps = hidx.lookup(target)
    hash_t = time.perf_counter() - t2
    return {
        "scan_steps": scan_steps,
        "bst_steps": bst_steps,
        "hash_steps": hash_steps,
        "scan_time": scan_t,
        "bst_time": bst_t,
        "hash_time": hash_t,
    }


if __name__ == "__main__":
    print(benchmark_lookup())
