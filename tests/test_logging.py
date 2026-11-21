import logging
from types import SimpleNamespace

import pytest

from system_resource_monitor import monitor
from system_resource_monitor.logger import save_measurement
from system_resource_monitor.report import generate_report


@pytest.mark.parametrize("usage", [89.9, 90, 95])
def test_sampling_logs_details_and_warns_at_threshold(monkeypatch, caplog, usage):
    sensor = SimpleNamespace(percent=usage, used=1, total=2)
    monkeypatch.setattr(monitor.psutil, "cpu_percent", lambda interval: usage)
    monkeypatch.setattr(monitor.psutil, "virtual_memory", lambda: sensor)
    monkeypatch.setattr(monitor.psutil, "disk_usage", lambda path: sensor)

    with caplog.at_level(logging.DEBUG, logger=monitor.__name__):
        measurement = monitor.get_system_info()

    assert (
        monitor.__name__,
        logging.DEBUG,
        f"Collected resource measurement: {measurement}",
    ) in caplog.record_tuples
    warnings = [
        record.getMessage()
        for record in caplog.records
        if record.levelno == logging.WARNING
    ]
    expected = [
        f"{resource} usage is high: {usage:.1f}%"
        for resource in ("CPU", "MEMORY", "DISK")
    ]
    assert warnings == (expected if usage >= 90 else [])


def test_sensor_failure_is_critical(monkeypatch, caplog):
    def unavailable_sensor(interval):
        raise OSError("sensor unavailable")

    monkeypatch.setattr(monitor.psutil, "cpu_percent", unavailable_sensor)

    with pytest.raises(OSError, match="sensor unavailable"):
        monitor.get_system_info()

    assert caplog.records[-1].levelno == logging.CRITICAL
    assert "Cannot collect a system resource measurement" in caplog.text


def test_csv_write_logs_success_and_failure(monkeypatch, tmp_path, caplog):
    monkeypatch.setattr(
        "system_resource_monitor.logger.get_system_info", lambda: {"cpu_percent": 10}
    )
    path = tmp_path / "metrics.csv"
    with caplog.at_level(logging.INFO):
        save_measurement(path)

    assert path.is_file()
    assert caplog.record_tuples[-1] == (
        "system_resource_monitor.logger",
        logging.INFO,
        f"Appended measurement to {path}",
    )

    with pytest.raises(FileNotFoundError):
        save_measurement(tmp_path / "missing" / "metrics.csv")

    assert caplog.records[-1].levelno == logging.ERROR
    assert "Cannot write measurement" in caplog.text


def test_invalid_report_logs_error(tmp_path, caplog):
    path = tmp_path / "invalid.csv"
    path.write_text("unexpected_column\n12\n", encoding="utf-8")

    with pytest.raises(KeyError, match="cpu_percent"):
        generate_report(path)

    assert caplog.records[-1].levelno == logging.ERROR
    assert f"Cannot summarize metrics CSV {path}" in caplog.text
