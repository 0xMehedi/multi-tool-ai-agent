from typing import Any, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from config.settings import DB_DIR
from tools.sql_executor import SQLiteManager


class DatabaseToolInput(BaseModel):
    question: str = Field(description="Natural language question about the data")
    sql_query: str = Field(description="SQLite query to execute")


class DatabaseTool(BaseTool):
    name: str = ""
    description: str = ""
    db_name: str = ""
    table_name: str = ""
    args_schema: Type[BaseModel] = DatabaseToolInput

    def _get_manager(self) -> SQLiteManager:
        db_path = DB_DIR / f"{self.db_name}.db"
        return SQLiteManager(db_path, self.table_name)

    def _run(self, question: str, sql_query: str) -> str:
        manager = self._get_manager()
        try:
            schema = manager.table_info()
            results = manager.execute_query(sql_query)
            if results and "error" in results[0]:
                return f"Error: {results[0]['error']}"
            if not results:
                return f"No results found for: {question}"
            formatted = []
            for row in results[:15]:
                formatted.append(str(row))
            return "\n".join(formatted)
        except Exception as exc:
            return f"Database error: {exc}"
        finally:
            manager.close()

    async def _arun(self, question: str, sql_query: str) -> str:
        return self._run(question, sql_query)
