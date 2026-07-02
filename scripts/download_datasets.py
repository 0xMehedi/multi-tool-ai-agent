from pathlib import Path

from config.logging_config import setup_logging
from config.settings import CSV_DIR, HUGGINGFACE_DATASETS, CSV_FILES

logger = setup_logging(__name__)


def download_dataset(dataset_name: str, dataset_path: str, output_path: Path) -> bool:
    try:
        from datasets import load_dataset

        logger.info("Downloading dataset: %s from %s", dataset_name, dataset_path)
        dataset = load_dataset(dataset_path, split="train")
        df = dataset.to_pandas()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(
            "Saved %s to %s (%d rows)", dataset_name, output_path, len(df)
        )
        return True
    except ImportError:
        logger.warning(
            "datasets library not installed. Install with: pip install datasets"
        )
        return False
    except Exception as exc:
        logger.error(
            "Failed to download dataset %s from %s: %s",
            dataset_name,
            dataset_path,
            exc,
        )
        return False


def download_all_datasets() -> bool:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    success = True
    for name, hf_path in HUGGINGFACE_DATASETS.items():
        output = CSV_FILES[name]
        if output.exists():
            logger.info("Dataset already exists at %s, skipping", output)
            continue
        ok = download_dataset(name, hf_path, output)
        if not ok:
            success = False
            logger.warning(
                "Manual download required for %s. Place CSV at %s",
                name,
                output,
            )
    return success


if __name__ == "__main__":
    download_all_datasets()
