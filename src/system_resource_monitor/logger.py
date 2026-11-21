import csv
import logging
from pathlib import Path

from .monitor import get_system_info

logger = logging.getLogger(__name__)


def save_measurement(filename="system_metrics.csv"):
    """Collect a system measurement and append it to a CSV file."""

    data = get_system_info()
    filepath = Path(filename)

    try:
        file_exists = filepath.exists() and filepath.stat().st_size > 0

        with filepath.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())

            if not file_exists:
                writer.writeheader()

            writer.writerow(data)
    except OSError as error:
        logger.error("Cannot write measurement to %s: %s", filepath, error)
        raise

    logger.info("Appended measurement to %s", filepath)
    print(f"Measurement saved to {filepath.resolve()}")


if __name__ == "__main__":
    save_measurement()
