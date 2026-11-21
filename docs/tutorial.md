# Record and interpret resource usage

In this walkthrough, you’ll check your current CPU, memory, and disk usage, save several measurements, and turn the recorded data into a summary.

## 1. Install the project

You’ll need Python 3.11 or newer and Poetry 2.2 or newer. Open a terminal in your project checkout. If you still need to clone the project or install Poetry, follow the [README installation instructions](../README.md#installation).

```bash
poetry install
```

Run the rest of the commands from the same directory. For a report containing only this session’s samples, start in a fresh checkout without an existing `system_metrics.csv`.

## 2. Check current usage

```bash
poetry run system-monitor status
```

The table shows CPU, memory, and root filesystem usage. Memory and disk also show used and total capacity. The timestamp below the table indicates when the sample was taken.

## 3. Save two measurements

```bash
poetry run system-monitor record
poetry run system-monitor record
```

The first run creates `system_metrics.csv` if it is missing. The second appends another row to the same file. Open the CSV in a text editor to see the header and a timestamp in each measurement row.

## 4. Collect measurements continuously

```bash
poetry run system-monitor watch --interval 2
```

Each sample is appended to the same CSV. The two-second delay starts after each sample, and CPU sampling itself takes about one second. Wait for a few save confirmations, then press **Ctrl+C**. The terminal displays `Monitoring stopped.`, and completed samples remain in the file.

## 5. Read the summary

```bash
poetry run system-monitor report
```

For each resource, **Average** is the arithmetic mean of the recorded percentages, **Minimum** is the lowest reading, and **Maximum** is the highest. Compare the average with the maximum to see how far the peak reading was above typical usage during your session. The **Total measurements** line counts the recorded samples. Activity between samples can be missed.

## Troubleshooting

- **The report cannot find the file.** Run `record` first and check that you are still in the same directory.
- **The report says there are no measurements or the CSV is invalid.** Record a sample into an empty CSV. If the existing file is malformed, rename it to keep a copy and record into a fresh file.
- **Recording cannot write the file.** Check that the directory is writable.
- **Watch rejects the interval.** Use a finite number greater than zero, such as `2`.
