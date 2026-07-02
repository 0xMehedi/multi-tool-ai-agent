from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy import types as sqltypes

from config.logging_config import setup_logging
from config.settings import CLEANED_CSV_FILES, DATABASES

logger = setup_logging(__name__)

TYPE_MAP = {
    "int64": sqltypes.INTEGER(),
    "int32": sqltypes.INTEGER(),
    "int16": sqltypes.INTEGER(),
    "int8": sqltypes.INTEGER(),
    "float64": sqltypes.REAL(),
    "float32": sqltypes.REAL(),
    "bool": sqltypes.BOOLEAN(),
    "object": sqltypes.TEXT(),
}


def map_dtype_to_sql(dtype: str) -> sqltypes.TypeEngine:
    dtype_lower = dtype.lower()
    if "int" in dtype_lower:
        return sqltypes.INTEGER()
    if "float" in dtype_lower:
        return sqltypes.REAL()
    if "bool" in dtype_lower:
        return sqltypes.BOOLEAN()
    return sqltypes.TEXT()


def csv_to_sqlite(
    csv_path: Path,
    db_path: Path,
    table_name: str,
) -> bool:
    try:
        logger.info("Converting %s to %s", csv_path, db_path)
        df = pd.read_csv(csv_path)

        db_path.parent.mkdir(parents=True, exist_ok=True)
        engine = create_engine(f"sqlite:///{db_path}")

        col_types = {}
        for col in df.columns:
            col_types[col] = map_dtype_to_sql(str(df[col].dtype))

        df.to_sql(table_name, engine, if_exists="replace", index=False, dtype=col_types)

        with engine.connect() as conn:
            insp = inspect(engine)
            columns = insp.get_columns(table_name)
            logger.info(
                "Table '%s' created with %d columns and %d rows",
                table_name,
                len(columns),
                len(df),
            )
            for col in columns:
                logger.debug(
                    "  Column: %s (%s)", col["name"], col["type"]
                )

        engine.dispose()
        logger.info("Successfully created database: %s", db_path)
        return True
    except Exception as exc:
        logger.error("Failed to convert %s: %s", csv_path, exc)
        return False


def convert_all() -> None:
    table_map = {
        "institutions": "institutions",
        "hospitals": "hospitals",
        "restaurants": "restaurants",
    }
    for name, table_name in table_map.items():
        csv_path = CLEANED_CSV_FILES[name]
        db_path = DATABASES[name]
        if not csv_path.exists():
            logger.warning("Cleaned CSV not found: %s", csv_path)
            continue
        csv_to_sqlite(csv_path, db_path, table_name)


if __name__ == "__main__":
    convert_all()
