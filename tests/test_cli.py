import sys
from unittest.mock import Mock

import pytest

from system_resource_monitor import cli, continuous


@pytest.mark.parametrize(
    ("arguments", "handler", "expected_args"),
    [
        (["status"], "display_system_info", ()),
        (["record"], "save_measurement", ("system_metrics.csv",)),
        (["record", "--file", "custom.csv"], "save_measurement", ("custom.csv",)),
        (["report"], "generate_report", ("system_metrics.csv",)),
        (["report", "--file", "custom.csv"], "generate_report", ("custom.csv",)),
        (["watch"], "continuous_monitoring", (5,)),
        (["watch", "--interval", "0.25"], "continuous_monitoring", (0.25,)),
    ],
)
def test_cli_dispatches_command(monkeypatch, arguments, handler, expected_args):
    command = Mock()
    monkeypatch.setattr(cli, handler, command)
    monkeypatch.setattr(sys, "argv", ["system-monitor", *arguments])

    cli.main()

    command.assert_called_once_with(*expected_args)


@pytest.mark.parametrize(
    "arguments", [[], ["unknown"], ["watch", "--interval", "soon"]]
)
def test_cli_rejects_invalid_arguments(monkeypatch, arguments):
    monkeypatch.setattr(sys, "argv", ["system-monitor", *arguments])

    with pytest.raises(SystemExit) as error:
        cli.main()

    assert error.value.code == 2


@pytest.mark.parametrize("interval", [0, -1, float("nan"), float("inf")])
def test_watch_rejects_invalid_interval_before_sampling(monkeypatch, interval):
    save = Mock()
    monkeypatch.setattr(continuous, "save_measurement", save)
    monkeypatch.setattr(continuous.time, "sleep", Mock(side_effect=KeyboardInterrupt))

    with pytest.raises(ValueError, match="Interval must be"):
        continuous.continuous_monitoring(interval)

    save.assert_not_called()


def test_watch_saves_a_sample_before_waiting_and_stops_on_interrupt(
    monkeypatch, capsys
):
    events = []

    def interrupt_after_sample(interval):
        events.append(("sleep", interval))
        raise KeyboardInterrupt

    monkeypatch.setattr(continuous, "save_measurement", lambda: events.append("save"))
    monkeypatch.setattr(continuous.time, "sleep", interrupt_after_sample)

    continuous.continuous_monitoring(0.25)

    assert events == ["save", ("sleep", 0.25)]
    assert "Monitoring stopped." in capsys.readouterr().out
