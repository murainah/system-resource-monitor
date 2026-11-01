# System Resource Monitor

A Python command-line application for monitoring CPU, memory, and disk usage. It supports real-time resource inspection, CSV logging, continuous monitoring, and statistical reporting.

The project uses **Poetry** as its build tool for dependency management, versioning, packaging, and running tasks.

## Features

- Display current CPU, memory, and disk usage.
- Save resource measurements to CSV.
- Continuously collect measurements at configurable intervals.
- Generate reports showing average, minimum, and maximum resource usage.

## Prerequisites

- Python 3.11 or newer
- [Poetry](https://python-poetry.org/docs/#installation) 2.2 or newer (needed for the `[dependency-groups]` section of `pyproject.toml`)

Check your versions:

```bash
python --version
poetry --version
```

## Quick Start

```bash
git clone https://github.com/murainah/system-resource-monitor.git
cd system-resource-monitor
poetry install
poetry run pytest
poetry build
```

These four commands install the dependencies, run the tests, and produce the distributable packages.

## Build Tool Usage

| Task | Command |
|---|---|
| Install dependencies and project | `poetry install` |
| Add a dependency | `poetry add <package>` |
| Add a development dependency | `poetry add --group dev <package>` |
| Update the lock file | `poetry lock` |
| Run the tests | `poetry run pytest` |
| Show the current version | `poetry version` |
| Bump the version | `poetry version patch` / `minor` / `major` |
| Build wheel and source distribution | `poetry build` |
| Run the application | `poetry run system-monitor status` |

### What Poetry automates

- **Dependency management:** runtime dependencies (`psutil`, `rich`, `pandas`) and development dependencies (`pytest`) are declared in `pyproject.toml`. `poetry.lock` pins exact versions so every install is reproducible.
- **Compilation / build:** Python has no separate compile step. `poetry build` is the build step: it assembles the source distribution and wheel from `src/`.
- **Version management:** the version lives in `pyproject.toml` and is changed with `poetry version`.
- **Packaging:** `poetry build` writes a wheel (`.whl`) and a source archive (`.tar.gz`) to `dist/`.
- **Entry point:** the `system-monitor` command is generated from `[project.scripts]`.

## Usage

Display current resource usage:

```bash
poetry run system-monitor status
```

Save a measurement to CSV (default file `system_metrics.csv`):

```bash
poetry run system-monitor record
poetry run system-monitor record --file metrics.csv
```

Generate a summary report from a CSV file:

```bash
poetry run system-monitor report
poetry run system-monitor report --file metrics.csv
```

Continuously record measurements (press Ctrl+C to stop):

```bash
poetry run system-monitor watch --interval 5
```

The interval is the delay after each measurement. Collecting CPU usage itself takes about one second.

## Building and Packaging

```bash
poetry build
```

The packages are written to `dist/`, for example:

```text
dist/system_resource_monitor-0.3.0-py3-none-any.whl
dist/system_resource_monitor-0.3.0.tar.gz
```

Verify the wheel in a clean virtual environment:

```bash
python -m venv /tmp/testenv
/tmp/testenv/bin/pip install dist/system_resource_monitor-0.3.0-py3-none-any.whl
/tmp/testenv/bin/system-monitor status
```

## Version Management

Show the current version:

```bash
poetry version
```

Release a new version, then commit and tag it:

```bash
poetry version minor
git commit -am "Bump version to 0.4.0"
git tag v0.4.0
git push origin main --tags
```

## Testing

The project uses pytest.

```bash
poetry run pytest
poetry run pytest -v
```

The tests check the structure of the collected system information, the presence of the required metrics, and that percentage values fall within valid ranges.

You can also check the command-line interface manually:

```bash
poetry run system-monitor --help
poetry run system-monitor status
```

## Project Structure

```text
system-resource-monitor/
├── pyproject.toml
├── poetry.lock
├── README.md
├── LICENSE
├── src/
│   └── system_resource_monitor/
│       ├── __init__.py
│       ├── monitor.py
│       ├── logger.py
│       ├── report.py
│       ├── continuous.py
│       └── cli.py
└── tests/
    ├── __init__.py
    └── test_monitor.py
```

## Technologies

- Python
- Poetry
- psutil
- Rich
- Pandas
- pytest

## Author

Abubakri Murainah

## License

MIT. See [LICENSE](LICENSE).