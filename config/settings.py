import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = PROJECT_ROOT / "data"
CSV_DIR: Path = DATA_DIR / "csv"
DB_DIR: Path = DATA_DIR / "db"
LOGS_DIR: Path = PROJECT_ROOT / "logs"

GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

LLM_MODEL: str = "models/gemini-2.0-flash"
LLM_TEMPERATURE: float = 0.1

DATABASES: dict[str, Path] = {
    "institutions": DB_DIR / "institutions.db",
    "hospitals": DB_DIR / "hospitals.db",
    "restaurants": DB_DIR / "restaurants.db",
}

HUGGINGFACE_DATASETS: dict[str, str] = {
    "institutions": "Mahadih534/Institutional-Information-of-Bangladesh",
    "hospitals": "Mahadih534/all-bangladeshi-hospitals",
    "restaurants": "Mahadih534/Bangladeshi-Restaurant-Data",
}

CSV_FILES: dict[str, Path] = {
    "institutions": CSV_DIR / "data.csv",
    "hospitals": CSV_DIR / "all-bangladesh-hosptals.csv",
    "restaurants": CSV_DIR / "restaurants.csv",
}

CLEANED_CSV_FILES: dict[str, Path] = {
    "institutions": CSV_DIR / "institutions_cleaned.csv",
    "hospitals": CSV_DIR / "hospitals_cleaned.csv",
    "restaurants": CSV_DIR / "restaurants_cleaned.csv",
}

LOG_FILE: Path = LOGS_DIR / "app.log"
LOG_LEVEL: str = "INFO"

ALLOWED_SQL_KEYWORDS: list[str] = [
    "SELECT", "COUNT", "AVG", "MIN", "MAX", "SUM",
    "GROUP BY", "ORDER BY", "LIMIT", "WHERE", "FROM",
    "JOIN", "LEFT", "RIGHT", "INNER", "ON", "AS",
    "AND", "OR", "NOT", "IN", "BETWEEN", "LIKE",
    "IS", "NULL", "DISTINCT",
]

BLOCKED_SQL_KEYWORDS: list[str] = [
    "DROP", "DELETE", "UPDATE", "INSERT", "ALTER",
    "TRUNCATE", "REPLACE", "ATTACH", "PRAGMA", "CREATE",
    "EXEC", "EXECUTE",
]
