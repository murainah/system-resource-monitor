
from system_resource_monitor.monitor import get_system_info


def test_system_info_returns_dictionary():
    info = get_system_info()

    assert isinstance(info, dict)


def test_system_info_contains_required_fields():
    info = get_system_info()

    expected_fields = [
        "timestamp",
        "cpu_percent",
        "memory_percent",
        "memory_used_gb",
        "memory_total_gb",
        "disk_percent",
        "disk_used_gb",
        "disk_total_gb",
    ]

    for field in expected_fields:
        assert field in info


def test_percentages_are_valid():
    info = get_system_info()

    for field in ["cpu_percent", "memory_percent", "disk_percent"]:
        assert 0 <= info[field] <= 100


def test_used_resources_do_not_exceed_total():
    info = get_system_info()

    assert info["memory_used_gb"] <= info["memory_total_gb"]
    assert info["disk_used_gb"] <= info["disk_total_gb"]
