"""Episode 06: Isolation levels. Runnable example in English."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class VersionedValue:
    txid: int
    value: int
    committed: bool


class VersionedKVStore:
    def __init__(self):
        self.data: dict[str, list[VersionedValue]] = {}
        self.next_txid = 1

    def begin(self) -> int:
        txid = self.next_txid
        self.next_txid += 1
        return txid

    def write(self, txid: int, key: str, value: int) -> None:
        self.data.setdefault(key, []).append(
            VersionedValue(txid=txid, value=value, committed=False)
        )

    def commit(self, txid: int) -> None:
        for versions in self.data.values():
            for v in versions:
                if v.txid == txid:
                    v.committed = True

    def rollback(self, txid: int) -> None:
        for key in list(self.data.keys()):
            self.data[key] = [v for v in self.data[key] if v.txid != txid]

    def read(
        self, txid: int, key: str, level: str, snapshot_tx: int | None = None
    ) -> int | None:
        versions = self.data.get(key, [])
        if level == "read_uncommitted":
            return versions[-1].value if versions else None
        visible = [v for v in versions if v.committed]
        if level == "repeatable_read" and snapshot_tx is not None:
            visible = [v for v in visible if v.txid <= snapshot_tx]
        if level == "serializable" and snapshot_tx is not None:
            visible = [v for v in visible if v.txid <= snapshot_tx]
        return visible[-1].value if visible else None


def phantom_read_demo(level: str) -> tuple[int, int]:
    rows: list[dict[str, int]] = [{"id": 1, "user_id": 7}]
    snapshot = list(rows)
    first = len([r for r in snapshot if r["user_id"] == 7])
    rows.append({"id": 2, "user_id": 7})
    if level in {"repeatable_read", "serializable"}:
        second = len([r for r in snapshot if r["user_id"] == 7])
    else:
        second = len([r for r in rows if r["user_id"] == 7])
    return first, second


if __name__ == "__main__":
    store = VersionedKVStore()
    t1 = store.begin()
    store.write(t1, "x", 10)
    t2 = store.begin()
    print(store.read(t2, "x", "read_uncommitted"))
