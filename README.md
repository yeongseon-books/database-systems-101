# database-systems-101 예제 코드

stdlib sqlite3 + 순수 Python으로 데이터베이스 핵심 개념을 실행 가능한 예제로 보여줍니다.

## 구성

- `ko/01-what-is-a-database.py`
- `ko/02-relational-model.py`
- `ko/03-sql-and-query-processing.py`
- `ko/04-indexes.py`
- `ko/05-transactions-and-acid.py`
- `ko/06-isolation-levels.py`
- `ko/07-normalization-and-modeling.py`
- `ko/08-query-optimization.py`
- `ko/09-replication-and-backup.py`
- `ko/10-oltp-and-olap.py`
- `en/`에는 동일 로직의 영어 주석 버전이 있습니다.
- `tests/`에는 에피소드별 동작 검증 테스트가 있습니다.

## 실행

```bash
pip install -r requirements.txt
python ko/01-what-is-a-database.py
python en/10-oltp-and-olap.py
```

## 테스트

```bash
pytest tests/ -q
```

## 원본

https://github.com/yeongseon-books/book-content/tree/master/content/database-systems-101
