from pathlib import Path

import pandas as pd

from config.logging_config import setup_logging
from config.settings import CSV_FILES, CLEANED_CSV_FILES

logger = setup_logging(__name__)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df.drop_duplicates()

    df = df.dropna(how="all")

    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace(["nan", "NaN", "None", "", "null", "NULL"], None)
        df[col] = df[col].str.replace(r"\s+", " ", regex=True)

    for col in df.columns:
        if df[col].dtype == "object":
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val[0])
            else:
                df[col] = df[col].fillna("Unknown")
        elif df[col].dtype in ("int64", "float64"):
            df[col] = df[col].fillna(0)

    return df


def clean_dataset(name: str, input_path: Path, output_path: Path) -> bool:
    try:
        logger.info("Cleaning dataset: %s", name)
        df = pd.read_csv(input_path)
        original_rows = len(df)
        df_clean = clean_dataframe(df)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df_clean.to_csv(output_path, index=False)
        removed = original_rows - len(df_clean)
        logger.info(
            "Cleaned %s: %d rows -> %d rows (%d removed)",
            name,
            original_rows,
            len(df_clean),
            removed,
        )
        return True
    except Exception as exc:
        logger.error("Failed to clean dataset %s: %s", name, exc)
        return False


def clean_all_datasets() -> None:
    for name in CSV_FILES:
        if not CSV_FILES[name].exists():
            logger.warning("Raw CSV not found: %s", CSV_FILES[name])
            continue
        clean_dataset(name, CSV_FILES[name], CLEANED_CSV_FILES[name])


if __name__ == "__main__":
    clean_all_datasets()
