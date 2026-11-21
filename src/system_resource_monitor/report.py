import logging
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()
logger = logging.getLogger(__name__)


def generate_report(filename="system_metrics.csv"):
    """Generate a summary of recorded system measurements."""

    filepath = Path(filename)

    if not filepath.exists():
        logger.error("Metrics file not found: %s", filepath)
        console.print("[red]No metrics file found.[/red]")
        return

    try:
        data = pd.read_csv(filepath)
    except (OSError, ValueError) as error:
        logger.error("Cannot read metrics CSV %s: %s", filepath, error)
        raise

    if data.empty:
        console.print("[yellow]No measurements available.[/yellow]")
        return

    metrics = {
        "CPU": "cpu_percent",
        "Memory": "memory_percent",
        "Disk": "disk_percent",
    }

    table = Table(title="System Resource Usage Report")

    table.add_column("Resource", style="cyan")
    table.add_column("Average (%)", justify="right")
    table.add_column("Minimum (%)", justify="right")
    table.add_column("Maximum (%)", justify="right")

    try:
        for name, column in metrics.items():
            table.add_row(
                name,
                f"{data[column].mean():.2f}",
                f"{data[column].min():.2f}",
                f"{data[column].max():.2f}",
            )
    except (KeyError, TypeError, ValueError) as error:
        logger.error("Cannot summarize metrics CSV %s: %s", filepath, error)
        raise

    console.print(table)
    console.print(f"\nTotal measurements: {len(data)}")


if __name__ == "__main__":
    generate_report()
