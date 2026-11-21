"""Collect CPU, memory, and root filesystem usage and display a live snapshot."""

import logging
from datetime import datetime

import psutil
from rich.console import Console
from rich.table import Table

console = Console()
logger = logging.getLogger(__name__)
HIGH_USAGE_PERCENT = 90
"""Usage percentage at or above which a resource warning is logged."""


def get_system_info():
    """Collect current resource usage, sampling CPU over one second.

    Returns a dictionary with a local ISO 8601 timestamp, CPU, memory, and
    disk percentages, and used and total memory and disk sizes in GiB. Size
    keys ending in `_gb` use 1024³ bytes per unit.

    Raises `OSError` if the operating system cannot supply a measurement
    or `psutil.Error` if a sensor query fails.
    """

    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
    except (OSError, psutil.Error):
        logger.critical("Cannot collect a system resource measurement", exc_info=True)
        raise

    data = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "cpu_percent": cpu_usage,
        "memory_percent": memory.percent,
        "memory_used_gb": round(memory.used / (1024**3), 2),
        "memory_total_gb": round(memory.total / (1024**3), 2),
        "disk_percent": disk.percent,
        "disk_used_gb": round(disk.used / (1024**3), 2),
        "disk_total_gb": round(disk.total / (1024**3), 2),
    }
    logger.debug("Collected resource measurement: %s", data)
    for resource in ("cpu", "memory", "disk"):
        usage = data[f"{resource}_percent"]
        if usage >= HIGH_USAGE_PERCENT:
            logger.warning("%s usage is high: %.1f%%", resource.upper(), usage)
    return data


def display_system_info():
    """Print a resource usage table and its timestamp.

    Sensor failures from `get_system_info` propagate to the caller.
    """

    data = get_system_info()

    table = Table(title="System Resource Monitor")

    table.add_column("Resource", style="cyan")
    table.add_column("Usage", style="green")
    table.add_column("Details")

    table.add_row("CPU", f"{data['cpu_percent']}%", "Processor usage")

    table.add_row(
        "Memory",
        f"{data['memory_percent']}%",
        f"{data['memory_used_gb']} / {data['memory_total_gb']} GB",
    )

    table.add_row(
        "Disk",
        f"{data['disk_percent']}%",
        f"{data['disk_used_gb']} / {data['disk_total_gb']} GB",
    )

    console.print(table)
    console.print(f"Timestamp: {data['timestamp']}")


if __name__ == "__main__":
    display_system_info()
