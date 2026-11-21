# System Resource Monitor

System Resource Monitor is a Python command-line tool for checking CPU, memory, and root filesystem usage. It can display a live snapshot, record samples to CSV, and report the average, minimum, and maximum usage for each resource.

## Installation

Install Python 3.11 or newer and [Poetry][poetry-install] 2.2 or newer. From a terminal, clone the project and install it with its dependencies.

```bash
git clone https://github.com/murainah/system-resource-monitor.git
cd system-resource-monitor
poetry install
```

## Usage

Run these commands from the project directory.

| Command | What it does |
|---|---|
| `poetry run system-monitor status` | Displays a snapshot of CPU, memory, and disk usage. |
| `poetry run system-monitor record` | Appends one sample to `system_metrics.csv`. |
| `poetry run system-monitor watch --interval 5` | Keeps appending samples to `system_metrics.csv` until you press Ctrl+C. |
| `poetry run system-monitor report` | Reads `system_metrics.csv` and prints the average, minimum, maximum, and sample count. |

CSV paths are relative to the current directory by default. Both `record` and `report` accept `--file` to use a different path.

```bash
poetry run system-monitor record --file metrics.csv
poetry run system-monitor report --file metrics.csv
```

The `watch` interval defaults to five seconds and must be finite and positive. It is the delay after each sample. Collecting CPU usage itself takes about one second. Run `poetry run system-monitor --help` to list the available commands and options.

## Logging

Diagnostics go to stderr and default to `WARNING`. Place `--log-level` before the command to change the minimum level.

```bash
poetry run system-monitor --log-level DEBUG status
poetry run system-monitor --log-level INFO record
```

- `DEBUG` shows the collected measurement values.
- `INFO` confirms that a sample was appended to a CSV.
- `WARNING` flags each resource whose usage is at least 90%.
- `ERROR` reports problems such as a missing, unreadable, or invalid CSV or a failed write.
- `CRITICAL` reports a sensor failure that prevents collecting a sample.

## Development checks

`poetry install` installs pytest, Ruff, and pre-commit in the project environment. The tests cover resource sampling, CSV recording and reports, CLI arguments, logging, and continuous monitoring using mocked sensors and temporary files.

```bash
poetry run pytest
poetry run ruff check .
poetry run ruff format --check .
```

Install the Git hook once per clone. It runs both Ruff checks on staged Python files before each commit. Use `--all-files` to check all tracked Python files immediately.

```bash
poetry run pre-commit install
poetry run pre-commit run --all-files
```

## Build the package

Run `poetry build` to create a wheel (`.whl`) and source distribution (`.tar.gz`) in `dist/`. Run `poetry version` to see the package version.

## Python reference

After `poetry install`, regenerate the API reference from the package docstrings.

```bash
poetry run pdoc -o docs/reference system_resource_monitor
```

Open the [reference index](docs/reference/index.html) from your local checkout in a browser.

## Project structure

| Path | Purpose |
|---|---|
| `src/system_resource_monitor/` | CLI, resource collection, CSV recording, continuous sampling, and report generation |
| `tests/` | pytest suite |
| `docs/reference/` | Generated Python API reference |
| `pyproject.toml` and `poetry.lock` | Package metadata, dependency versions, and Ruff configuration |
| `.pre-commit-config.yaml` | Ruff checks run by the Git hook |

## Troubleshooting

- **Poetry is missing or rejects `dependency-groups`.** Verify the installed version with `poetry --version` and follow the [Poetry installation guide][poetry-install] to install or update it.
- **The report cannot find the CSV.** Run `record` first, use the same working directory, and pass the same `--file` path to both commands when using a custom filename.
- **The report says no measurements are available.** Record a sample to populate the CSV. For an invalid CSV, use a file produced by `record` or `watch`.
- **Recording fails to write a CSV.** Check that the parent directory exists and that you have permission to write there.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

[Abubakri Murainah](https://github.com/murainah)

[poetry-install]: https://python-poetry.org/docs/#installation
