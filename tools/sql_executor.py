from pathlib import Path
from typing import Any, Optional

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

from config.logging_config import setup_logging
from tools.helper import validate_sql_query, format_table_info

logger = setup_logging(__name__)


class SQLiteManager:
    def __init__(self, db_path: Path, table_name: str) -> None:
        self.db_path: Path = db_path
        self.table_name: str = table_name
        self._engine: Optional[Engine] = None

    def _get_engine(self) -> Engine:
        if self._engine is None:
            self._engine = create_engine(
                f"sqlite:///{self.db_path}",
                echo=False,
            )
        return self._engine

    def execute_query(self, sql: str) -> list[dict[str, Any]]:
        if not validate_sql_query(sql):
            logger.warning("Blocked or invalid SQL: %s", sql)
            return [{"error": "Only SELECT queries are allowed."}]

        engine = self._get_engine()
        try:
            with engine.connect() as conn:
                result = conn.execute(text(sql))
                rows = result.fetchall()
                columns = result.keys()
                return [dict(zip(columns, row)) for row in rows]
        except Exception as exc:
            logger.error("SQL execution error: %s", exc)
            return [{"error": f"SQL execution failed: {exc}"}]

    def get_schema(self) -> list[dict[str, Any]]:
        engine = self._get_engine()
        try:
            insp = inspect(engine)
            columns = insp.get_columns(self.table_name)
            return [
                {
                    "name": col["name"],
                    "type": str(col["type"]),
                    "nullable": col.get("nullable", True),
                }
                for col in columns
            ]
        except Exception as exc:
            logger.error("Schema fetch error: %s", exc)
            return []

    def table_info(self) -> str:
        schema = self.get_schema()
        return format_table_info(schema, self.table_name)

    def sample_rows(self, n: int = 3) -> list[dict[str, Any]]:
        return self.execute_query(f"SELECT * FROM {self.table_name} LIMIT {n}")

    def close(self) -> None:
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None
