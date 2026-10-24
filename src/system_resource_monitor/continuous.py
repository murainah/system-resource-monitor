
import time

from rich.console import Console

from .logger import save_measurement


console = Console()


def continuous_monitoring(interval=5):
    """Record system measurements repeatedly."""

    if interval <= 0:
        raise ValueError("Interval must be greater than zero.")

    console.print(
        f"[green]Monitoring started. "
        f"Interval: {interval} seconds.[/green]"
    )
    console.print("Press Ctrl+C to stop.\n")

    try:
        while True:
            save_measurement()
            time.sleep(interval)

    except KeyboardInterrupt:
        console.print("\n[yellow]Monitoring stopped.[/yellow]")


if __name__ == "__main__":
    continuous_monitoring()
