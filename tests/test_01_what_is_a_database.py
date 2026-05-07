from pathlib import Path

from conftest import load_ko_module


def test_file_persistence_and_memory_db(tmp_path: Path):
    m = load_ko_module("01-what-is-a-database.py")
    json_path = tmp_path / "accounts.json"
    m.flat_file_deposit(json_path, "u1", 10)
    m.flat_file_deposit(json_path, "u1", 5)
    assert '"u1": 15' in json_path.read_text()
    rows = m.sqlite_memory_demo()
    assert rows == [("alice", 150)]


def test_file_db_persists_across_connections(tmp_path: Path):
    m = load_ko_module("01-what-is-a-database.py")
    first, second = m.sqlite_file_persistence_demo(tmp_path / "ep01.db")
    assert first == second == 1
