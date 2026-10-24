
import psutil
from datetime import datetime
from rich.console import Console
from rich.table import Table


console = Console()


def get_system_info():
    """Collect current CPU, memory, and disk usage."""

    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "cpu_percent": cpu_usage,
        "memory_percent": memory.percent,
        "memory_used_gb": round(memory.used / (1024 ** 3), 2),
        "memory_total_gb": round(memory.total / (1024 ** 3), 2),
        "disk_percent": disk.percent,
        "disk_used_gb": round(disk.used / (1024 ** 3), 2),
        "disk_total_gb": round(disk.total / (1024 ** 3), 2),
    }


def display_system_info():
    """Display system information in a formatted table."""

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
