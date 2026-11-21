import csv
import re

import pytest
from pandas.errors import ParserError
from rich.console import Console

from system_resource_monitor import logger, report

HEADER = "cpu_percent,memory_percent,disk_percent\n"


@pytest.mark.parametrize("existing_empty_file", [False, True])
def test_save_writes_one_header_and_appends_measurements(
    tmp_path, monkeypatch, existing_empty_file
):
    path = tmp_path / "metrics.csv"
    if existing_empty_file:
        path.touch()
    readings = iter(
        [
            {"cpu_percent": 10, "memory_percent": 40, "disk_percent": 70},
            {"cpu_percent": 30, "memory_percent": 50, "disk_percent": 80},
        ]
    )
    monkeypatch.setattr(logger, "get_system_info", lambda: next(readings))

    logger.save_measurement(path)
    assert path.read_text() == HEADER + "10,40,70\n"
    logger.save_measurement(path)

    with path.open(newline="", encoding="utf-8") as file:
        assert list(csv.reader(file)) == [
            ["cpu_percent", "memory_percent", "disk_percent"],
            ["10", "40", "70"],
            ["30", "50", "80"],
        ]


def test_report_shows_statistics_and_sample_count(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(report, "console", Console(width=100))
    path = tmp_path / "metrics.csv"
    path.write_text(HEADER + "10,40,70\n30,50,80\n", encoding="utf-8")

    report.generate_report(path)

    output = capsys.readouterr().out
    assert re.search(r"CPU\s*│\s*20\.00\s*│\s*10\.00\s*│\s*30\.00", output)
    assert re.search(r"Memory\s*│\s*45\.00\s*│\s*40\.00\s*│\s*50\.00", output)
    assert re.search(r"Disk\s*│\s*75\.00\s*│\s*70\.00\s*│\s*80\.00", output)
    assert "Total measurements: 2" in output


def test_report_explains_missing_file(tmp_path, capsys):
    report.generate_report(tmp_path / "missing.csv")

    assert "No metrics file found." in capsys.readouterr().out


@pytest.mark.parametrize("content", ["", HEADER])
def test_report_explains_empty_file(tmp_path, capsys, content):
    path = tmp_path / "empty.csv"
    path.write_text(content, encoding="utf-8")

    report.generate_report(path)

    assert "No measurements available." in capsys.readouterr().out


def test_report_rejects_malformed_csv(tmp_path):
    path = tmp_path / "malformed.csv"
    path.write_text(HEADER + '"unclosed,40,70\n', encoding="utf-8")

    with pytest.raises(ParserError):
        report.generate_report(path)
