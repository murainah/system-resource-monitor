import argparse
import logging

from .continuous import continuous_monitoring
from .logger import save_measurement
from .monitor import display_system_info
from .report import generate_report


def main():
    """Command-line interface for System Resource Monitor."""

    parser = argparse.ArgumentParser(description="Monitor CPU, memory, and disk usage.")
    parser.add_argument(
        "--log-level",
        type=str.upper,
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
        default="WARNING",
        help="Minimum diagnostic level (default: WARNING)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Display current system resource usage")

    record_parser = subparsers.add_parser(
        "record", help="Save a system measurement to CSV"
    )
    record_parser.add_argument(
        "--file", default="system_metrics.csv", help="Output CSV filename"
    )

    report_parser = subparsers.add_parser(
        "report", help="Generate a resource usage summary"
    )
    report_parser.add_argument(
        "--file", default="system_metrics.csv", help="Input CSV filename"
    )

    watch_parser = subparsers.add_parser(
        "watch", help="Continuously record system measurements"
    )
    watch_parser.add_argument(
        "--interval", type=float, default=5, help="Seconds to wait between measurements"
    )

    args = parser.parse_args()
    logging.basicConfig(
        level=args.log_level, format="%(levelname)s %(name)s: %(message)s"
    )

    if args.command == "status":
        display_system_info()

    elif args.command == "record":
        save_measurement(args.file)

    elif args.command == "report":
        generate_report(args.file)

    elif args.command == "watch":
        continuous_monitoring(args.interval)


if __name__ == "__main__":
    main()
