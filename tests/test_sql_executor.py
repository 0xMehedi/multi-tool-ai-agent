import pytest
from pathlib import Path
import tempfile
import pandas as pd
from tools.sql_executor import SQLiteManager


@pytest.fixture
def db_manager():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["A", "B", "C"],
            "value": [10.5, 20.3, 30.7],
            "city": ["Dhaka", "Chattogram", "Dhaka"],
        })
        engine = __import__("sqlalchemy").create_engine(f"sqlite:///{db_path}")
        df.to_sql("test_table", engine, if_exists="replace", index=False)
        engine.dispose()

        manager = SQLiteManager(db_path, "test_table")
        yield manager
        manager.close()


class TestSQLiteManager:
    def test_execute_select_all(self, db_manager):
        results = db_manager.execute_query("SELECT * FROM test_table ORDER BY id")
        assert len(results) == 3
        assert results[0]["name"] == "A"

    def test_execute_with_where(self, db_manager):
        results = db_manager.execute_query(
            "SELECT * FROM test_table WHERE city = 'Dhaka'"
        )
        assert len(results) == 2

    def test_execute_aggregate(self, db_manager):
        results = db_manager.execute_query(
            "SELECT COUNT(*) as cnt FROM test_table"
        )
        assert results[0]["cnt"] == 3

    def test_execute_avg(self, db_manager):
        results = db_manager.execute_query(
            "SELECT AVG(value) as avg_val FROM test_table"
        )
        assert abs(results[0]["avg_val"] - 20.5) < 0.1

    def test_blocked_query(self, db_manager):
        results = db_manager.execute_query("DROP TABLE test_table")
        assert "error" in results[0]

    def test_get_schema(self, db_manager):
        schema = db_manager.get_schema()
        assert len(schema) == 4
        col_names = [col["name"] for col in schema]
        assert "id" in col_names
        assert "name" in col_names
        assert "value" in col_names
        assert "city" in col_names

    def test_table_info(self, db_manager):
        info = db_manager.table_info()
        assert "test_table" in info

    def test_close(self, db_manager):
        db_manager.close()
        assert db_manager._engine is None
