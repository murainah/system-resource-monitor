from datetime import datetime
from types import SimpleNamespace

from system_resource_monitor import monitor


def test_system_info_maps_sensor_values_and_converts_sizes(monkeypatch):
    gib = 1024**3

    def cpu_percent(*, interval):
        assert interval == 1
        return 12.5

    def disk_usage(path):
        assert path == "/"
        return SimpleNamespace(percent=75.0, used=6 * gib, total=8 * gib)

    monkeypatch.setattr(monitor.psutil, "cpu_percent", cpu_percent)
    monkeypatch.setattr(
        monitor.psutil,
        "virtual_memory",
        lambda: SimpleNamespace(percent=37.5, used=3 * gib // 2, total=4 * gib),
    )
    monkeypatch.setattr(monitor.psutil, "disk_usage", disk_usage)

    info = monitor.get_system_info()
    timestamp = info.pop("timestamp")
    assert datetime.fromisoformat(timestamp).isoformat(timespec="seconds") == timestamp
    assert info == {
        "cpu_percent": 12.5,
        "memory_percent": 37.5,
        "memory_used_gb": 1.5,
        "memory_total_gb": 4.0,
        "disk_percent": 75.0,
        "disk_used_gb": 6.0,
        "disk_total_gb": 8.0,
    }
