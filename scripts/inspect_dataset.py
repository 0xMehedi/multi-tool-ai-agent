from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from config.logging_config import setup_logging
from config.settings import CSV_FILES

logger = setup_logging(__name__)
console = Console()


def inspect_csv(file_path: Path) -> dict:
    df = pd.read_csv(file_path)
    report = {
        "file": file_path.name,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "missing_pct": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
        "duplicate_rows": df.duplicated().sum(),
        "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB",
    }
    return report


def display_report(report: dict) -> None:
    file_panel = Panel(
        f"[bold cyan]{report['file']}[/bold cyan]\n"
        f"[green]Rows:[/green] {report['rows']}\n"
        f"[green]Columns:[/green] {report['columns']}\n"
        f"[green]Duplicate Rows:[/green] {report['duplicate_rows']}\n"
        f"[green]Memory:[/green] {report['memory_usage']}",
        title="Dataset Overview",
    )
    console.print(file_panel)

    col_table = Table(title="Column Details", show_header=True)
    col_table.add_column("Column Name", style="cyan")
    col_table.add_column("Data Type", style="magenta")
    col_table.add_column("Missing", style="yellow")
    col_table.add_column("Missing %", style="red")
    for col in report["column_names"]:
        col_table.add_row(
            col,
            report["dtypes"].get(col, "unknown"),
            str(report["missing_values"].get(col, 0)),
            f"{report['missing_pct'].get(col, 0)}%",
        )
    console.print(col_table)


def inspect_all() -> None:
    for name, path in CSV_FILES.items():
        if not path.exists():
            logger.warning("File not found: %s", path)
            continue
        report = inspect_csv(path)
        display_report(report)
        console.print()


if __name__ == "__main__":
    inspect_all()
