import pytest
from tools.helper import validate_sql_query, sanitize_sql, serialize_results, format_table_info


class TestValidateSQLQuery:
    def test_valid_select(self):
        assert validate_sql_query("SELECT * FROM hospitals") is True

    def test_valid_select_with_where(self):
        assert validate_sql_query("SELECT name FROM hospitals WHERE district = 'Dhaka'") is True

    def test_valid_aggregate(self):
        assert validate_sql_query("SELECT COUNT(*) FROM institutions") is True

    def test_blocked_drop(self):
        assert validate_sql_query("DROP TABLE hospitals") is False

    def test_blocked_delete(self):
        assert validate_sql_query("DELETE FROM hospitals") is False

    def test_blocked_update(self):
        assert validate_sql_query("UPDATE hospitals SET name = 'test'") is False

    def test_blocked_insert(self):
        assert validate_sql_query("INSERT INTO hospitals VALUES (1)") is False

    def test_blocked_alter(self):
        assert validate_sql_query("ALTER TABLE hospitals ADD COLUMN test") is False

    def test_blocked_truncate(self):
        assert validate_sql_query("TRUNCATE hospitals") is False

    def test_blocked_replace(self):
        assert validate_sql_query("REPLACE INTO hospitals VALUES (1)") is False

    def test_blocked_attach(self):
        assert validate_sql_query("ATTACH DATABASE 'test.db' AS test") is False

    def test_blocked_pragma(self):
        assert validate_sql_query("PRAGMA journal_mode=WAL") is False

    def test_non_select_statement(self):
        assert validate_sql_query("WITH cte AS (SELECT * FROM t) SELECT * FROM cte") is True


class TestSanitizeSQL:
    def test_sanitize_drop(self):
        result = sanitize_sql("DROP TABLE hospitals")
        assert "-- BLOCKED" in result

    def test_sanitize_clean(self):
        result = sanitize_sql("SELECT * FROM hospitals")
        assert result == "SELECT * FROM hospitals"


class TestSerializeResults:
    def test_empty_results(self):
        assert serialize_results([]) == "No results found."

    def test_single_result(self):
        results = [{"name": "DMCH", "beds": 1000}]
        serialized = serialize_results(results)
        assert "name: DMCH" in serialized
        assert "beds: 1000" in serialized

    def test_multiple_results(self):
        results = [
            {"name": "Hospital A", "district": "Dhaka"},
            {"name": "Hospital B", "district": "Chattogram"},
        ]
        serialized = serialize_results(results)
        assert "Hospital A" in serialized
        assert "Hospital B" in serialized


class TestFormatTableInfo:
    def test_format_table_info(self):
        schema = [
            {"name": "id", "type": "INTEGER", "nullable": False},
            {"name": "name", "type": "TEXT", "nullable": True},
        ]
        result = format_table_info(schema, "hospitals")
        assert "Table: hospitals" in result
        assert "id (INTEGER)" in result
        assert "name (TEXT)" in result
