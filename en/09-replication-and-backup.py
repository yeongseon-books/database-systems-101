"""Episode 09: Replication and backup. Runnable example in English."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Op:
    lsn: int
    key: str
    value: int


class Node:
    def __init__(self):
        self.data: dict[str, int] = {}
        self.applied_lsn = 0

    def apply(self, op: Op) -> None:
        self.data[op.key] = op.value
        self.applied_lsn = op.lsn


class LeaderFollowerReplication:
    def __init__(self, followers: int = 2):
        self.leader = Node()
        self.followers = [Node() for _ in range(followers)]
        self.log: list[Op] = []

    def write(self, key: str, value: int) -> Op:
        op = Op(lsn=len(self.log) + 1, key=key, value=value)
        self.log.append(op)
        self.leader.apply(op)
        return op

    def replicate_step(self, follower_idx: int, steps: int = 1) -> None:
        follower = self.followers[follower_idx]
        for op in self.log[follower.applied_lsn : follower.applied_lsn + steps]:
            follower.apply(op)

    def replay_until(self, pitr_lsn: int) -> Node:
        recovered = Node()
        for op in self.log:
            if op.lsn <= pitr_lsn:
                recovered.apply(op)
        return recovered

    def lag(self, follower_idx: int) -> int:
        return len(self.log) - self.followers[follower_idx].applied_lsn


if __name__ == "__main__":
    rf = LeaderFollowerReplication()
    rf.write("counter", 1)
    rf.replicate_step(0)
    print(rf.lag(0))
