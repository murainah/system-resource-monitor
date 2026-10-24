
import csv
from pathlib import Path

from .monitor import get_system_info


def save_measurement(filename="system_metrics.csv"):
    """Collect a system measurement and append it to a CSV file."""

    data = get_system_info()
    filepath = Path(filename)

    file_exists = filepath.exists() and filepath.stat().st_size > 0

    with filepath.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)

    print(f"Measurement saved to {filepath.resolve()}")


if __name__ == "__main__":
    save_measurement()
