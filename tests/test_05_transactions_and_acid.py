from pathlib import Path

from conftest import load_ko_module


def test_rollback_and_commit(tmp_path: Path):
    m = load_ko_module("05-transactions-and-acid.py")
    db_path = tmp_path / "bank.db"
    m.init_bank(db_path)
    m.transfer(db_path, 1, 2, 100)
    assert m.balances(db_path) == {"Alice": 900, "Bob": 1100}
    try:
        m.transfer(db_path, 1, 2, 50, fail_midway=True)
    except RuntimeError:
        pass
    assert m.balances(db_path) == {"Alice": 900, "Bob": 1100}


def test_toy_wal_replay():
    m = load_ko_module("05-transactions-and-acid.py")
    wal = m.ToyWAL()
    wal.append_transfer("Alice", "Bob", 100)
    wal.apply()
    assert wal.state == {"Alice": 900, "Bob": 1100}
