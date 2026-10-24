
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table


console = Console()


def generate_report(filename="system_metrics.csv"):
    """Generate a summary of recorded system measurements."""

    filepath = Path(filename)

    if not filepath.exists():
        console.print("[red]No metrics file found.[/red]")
        return

    data = pd.read_csv(filepath)

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

    for name, column in metrics.items():
        table.add_row(
            name,
            f"{data[column].mean():.2f}",
            f"{data[column].min():.2f}",
            f"{data[column].max():.2f}",
        )

    console.print(table)
    console.print(f"\nTotal measurements: {len(data)}")


if __name__ == "__main__":
    generate_report()
