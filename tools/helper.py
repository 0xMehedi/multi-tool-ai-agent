import re
from typing import Any

from config.settings import ALLOWED_SQL_KEYWORDS, BLOCKED_SQL_KEYWORDS


def validate_sql_query(sql: str) -> bool:
    sql_upper = sql.upper().strip()

    for blocked in BLOCKED_SQL_KEYWORDS:
        pattern = r"\b" + re.escape(blocked) + r"\b"
        if re.search(pattern, sql_upper):
            return False

    if not (sql_upper.startswith("SELECT") or sql_upper.startswith("WITH")):
        return False

    if sql_upper.startswith("WITH") and "SELECT" not in sql_upper:
        return False

    return True


def sanitize_sql(sql: str) -> str:
    sql_upper = sql.upper().strip()
    for blocked in BLOCKED_SQL_KEYWORDS:
        pattern = re.compile(r"\b" + re.escape(blocked) + r"\b", re.IGNORECASE)
        sql = pattern.sub("-- BLOCKED", sql)
    return sql


def serialize_results(results: list[dict[str, Any]]) -> str:
    if not results:
        return "No results found."
    lines: list[str] = []
    for row in results[:20]:
        items = [f"{k}: {v}" for k, v in row.items()]
        lines.append(" | ".join(items))
    return "\n".join(lines)


def format_table_info(schema: list[dict[str, Any]], table_name: str) -> str:
    cols = []
    for col in schema:
        cols.append(f"  - {col['name']} ({col['type']})")
    return f"Table: {table_name}\nColumns:\n" + "\n".join(cols)
