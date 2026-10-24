
# System Resource Monitor

A Python command-line application for monitoring CPU, memory, and disk usage. The application supports real-time resource inspection, CSV logging, continuous monitoring, and statistical reporting.

## Features

- Display current CPU, memory, and disk usage.
- Save resource measurements to CSV.
- Continuously collect measurements at configurable intervals.
- Generate reports showing average, minimum, and maximum resource usage.
- Manage dependencies, versions, and packaging using Poetry.

## Technologies

- Python 3.14
- Poetry
- psutil
- Rich
- Pandas

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/system-resource-monitor.git
cd system-resource-monitor
```

Install the dependencies and project:

```bash
poetry install
```

## Usage

Display current resource usage:

```bash
poetry run system-monitor status
```

Save a measurement to CSV:

```bash
poetry run system-monitor record
```

Save a measurement to a custom file:

```bash
poetry run system-monitor record --file metrics.csv
```

Generate a summary report:

```bash
poetry run system-monitor report
```

Continuously record measurements:

```bash
poetry run system-monitor watch --interval 5
```

Press Ctrl+C to stop continuous monitoring.

The interval specifies the delay after each measurement. Collecting CPU usage itself takes approximately one second.

## Building the Project

Build the wheel and source distribution:

```bash
poetry build
```

The generated packages are saved in `dist/`.

## Version Management

Display the current project version:

```bash
poetry version
```

Increase the minor version:

```bash
poetry version minor
```

## Testing

Verify the command-line interface:

```bash
poetry run system-monitor --help
poetry run system-monitor status
```

To verify the generated wheel, install it into a separate virtual environment and run the installed command.

## Project Structure

```text
system-resource-monitor/
├── pyproject.toml
├── poetry.lock
├── README.md
├── src/
│   └── system_resource_monitor/
│       ├── __init__.py
│       ├── monitor.py
│       ├── logger.py
│       ├── report.py
│       ├── continuous.py
│       └── cli.py
└── tests/
```

## Build Automation

Poetry is used for:

- Dependency management through `pyproject.toml`.
- Reproducible dependency resolution through `poetry.lock`.
- Project version management.
- Wheel and source distribution packaging.
- Installing and executing the application.



## Running Tests

This project uses pytest for automated testing.

Install the project and development dependencies:

```bash
poetry install
```

Run all tests:

```bash
poetry run pytest
```

Run tests with detailed output:

```bash
poetry run pytest -v
```

The tests verify the structure of the system information, required metrics, valid percentage ranges, and resource usage values.


## Author

Abubakri Murainah

## Version

0.3.0
