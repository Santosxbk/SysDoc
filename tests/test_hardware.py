from types import SimpleNamespace

from sysdoc.hardware.monitor import get_battery_info, get_gpu_info, get_temperature_info


def test_hardware_helpers_return_expected_shapes() -> None:
    gpu = get_gpu_info()
    battery = get_battery_info()
    temperatures = get_temperature_info()

    assert isinstance(gpu["model"], str)
    assert isinstance(gpu["memory_mb"], int)
    assert isinstance(battery["available"], bool)
    assert isinstance(battery["percent"], int)
    assert isinstance(temperatures["available"], bool)
    assert isinstance(temperatures["readings"], list)


def test_gpu_info_detects_nvidia(monkeypatch) -> None:
    def fake_run(cmd, capture_output, text, check, timeout=None):
        executable = cmd[0].split("/")[-1]
        if executable == "nvidia-smi" and cmd[1] == "--query-gpu=name":
            return SimpleNamespace(stdout="NVIDIA GeForce RTX 4070\n", returncode=0)
        if executable == "nvidia-smi" and cmd[1] == "--query-gpu=memory.total":
            return SimpleNamespace(stdout="12282 MiB\n", returncode=0)
        if executable == "nvidia-smi" and cmd[1] == "--query-gpu=driver_version":
            return SimpleNamespace(stdout="550.54.14\n", returncode=0)
        return SimpleNamespace(stdout="", returncode=1)

    monkeypatch.setattr("sysdoc.hardware.monitor.shutil.which", lambda name: "/usr/bin/nvidia-smi" if name == "nvidia-smi" else None)
    monkeypatch.setattr("sysdoc.hardware.monitor.subprocess.run", fake_run)

    gpu = get_gpu_info()

    assert gpu["available"] is True
    assert "NVIDIA" in gpu["model"]
    assert gpu["memory_mb"] > 0
    assert gpu["driver"] == "550.54.14"


def test_battery_info_handles_missing_seconds_left(monkeypatch) -> None:
    battery = SimpleNamespace(percent=60, power_plugged=True, secsleft=None)
    monkeypatch.setattr("sysdoc.hardware.monitor.psutil.sensors_battery", lambda: battery)

    info = get_battery_info()

    assert info["available"] is True
    assert info["percent"] == 60
    assert info["plugged"] is True
    assert info["remaining_hours"] == 0.0


def test_temperature_info_ignores_missing_numeric_values(monkeypatch) -> None:
    temps = {
        "coretemp": [
            SimpleNamespace(current=None, high=None),
            SimpleNamespace(current=57.3, high=93.5),
        ]
    }
    monkeypatch.setattr("sysdoc.hardware.monitor.psutil.sensors_temperatures", lambda: temps)

    info = get_temperature_info()

    assert info["available"] is True
    assert info["readings"][0]["current"] is None
    assert info["readings"][1]["current"] == 57.3
