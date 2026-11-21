"""Record resource measurements periodically until interrupted."""

import math
import time

from rich.console import Console

from .logger import save_measurement

console = Console()


def continuous_monitoring(interval=5):
    """Append samples to `system_metrics.csv` in the current directory.

    `interval` is the delay in seconds after each completed sample. It must
    be finite and greater than zero.

    Returns `None` after a keyboard interrupt stops monitoring.

    Raises `ValueError` for an invalid interval, `OSError` for an OS error
    during collection or writing, or `psutil.Error` for a failed sensor query.
    """

    if not math.isfinite(interval) or interval <= 0:
        raise ValueError("Interval must be finite and greater than zero.")

    console.print(f"[green]Monitoring started. Interval: {interval} seconds.[/green]")
    console.print("Press Ctrl+C to stop.\n")

    try:
        while True:
            save_measurement()
            time.sleep(interval)

    except KeyboardInterrupt:
        console.print("\n[yellow]Monitoring stopped.[/yellow]")


if __name__ == "__main__":
    continuous_monitoring()
