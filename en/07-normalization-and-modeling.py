"""Episode 07: Normalization and modeling. Runnable example in English."""
from __future__ import annotations

from itertools import combinations


FD = tuple[frozenset[str], frozenset[str]]


def closure(attrs: frozenset[str], fds: list[FD]) -> frozenset[str]:
    result = set(attrs)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs.issubset(result) and not rhs.issubset(result):
                result |= rhs
                changed = True
    return frozenset(result)


def candidate_keys(relation: frozenset[str], fds: list[FD]) -> list[frozenset[str]]:
    attrs = sorted(relation)
    keys = []
    for r in range(1, len(attrs) + 1):
        for combo in combinations(attrs, r):
            c = frozenset(combo)
            if closure(c, fds) == relation and not any(k.issubset(c) for k in keys):
                keys.append(c)
    return keys


def synthesize_3nf(relation: frozenset[str], fds: list[FD]) -> list[frozenset[str]]:
    schemas = [lhs | rhs for lhs, rhs in fds]
    keys = candidate_keys(relation, fds)
    if keys and not any(keys[0].issubset(s) for s in schemas):
        schemas.append(keys[0])
    unique = []
    for s in schemas:
        if not any(s <= u for u in unique):
            unique.append(s)
    return unique


def is_dependency_preserved(decomposition: list[frozenset[str]], fds: list[FD]) -> bool:
    return all(any((lhs | rhs).issubset(r) for r in decomposition) for lhs, rhs in fds)


if __name__ == "__main__":
    R = frozenset({"order_id", "user_id", "user_email", "product_id", "product_name"})
    F = [
        (frozenset({"order_id"}), frozenset({"user_id"})),
        (frozenset({"user_id"}), frozenset({"user_email"})),
        (frozenset({"product_id"}), frozenset({"product_name"})),
    ]
    print(synthesize_3nf(R, F))
