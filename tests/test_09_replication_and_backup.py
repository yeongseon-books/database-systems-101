from conftest import load_ko_module


def test_follower_catches_up_and_pitr_works():
    m = load_ko_module("09-replication-and-backup.py")
    rf = m.LeaderFollowerReplication(followers=1)
    rf.write("counter", 1)
    rf.write("counter", 2)
    assert rf.lag(0) == 2
    rf.replicate_step(0, steps=2)
    assert rf.lag(0) == 0
    recovered = rf.replay_until(1)
    assert recovered.data["counter"] == 1
