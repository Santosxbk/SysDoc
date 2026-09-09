"""Hardware monitoring helpers for GPU, battery and temperature data."""

from __future__ import annotations

import logging
import platform
import shutil
import subprocess
from typing import Any

import psutil

logger = logging.getLogger(__name__)


def get_gpu_info() -> dict[str, Any]:
    """Return a best-effort GPU summary."""

    try:
        gpu_executable = shutil.which("nvidia-smi")
        if gpu_executable:
            name = subprocess.run(
                [gpu_executable, "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                check=False,
                timeout=5,
            )
            memory_total = subprocess.run(
                [gpu_executable, "--query-gpu=memory.total", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                check=False,
                timeout=5,
            )
            driver = subprocess.run(
                [gpu_executable, "--query-gpu=driver_version", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                check=False,
                timeout=5,
            )

            model_name = name.stdout.strip().splitlines()[0].strip() if name.returncode == 0 and name.stdout.strip() else "Unknown"
            memory_value = memory_total.stdout.strip().splitlines()[0].strip() if memory_total.returncode == 0 and memory_total.stdout.strip() else "0"
            driver_value = driver.stdout.strip().splitlines()[0].strip() if driver.returncode == 0 and driver.stdout.strip() else "Unknown"

            memory_mb = 0
            if memory_value:
                digits = "".join(ch for ch in memory_value if ch.isdigit())
                if digits:
                    memory_mb = int(digits)

            return {
                "model": model_name if model_name != "Unknown" else platform.machine(),
                "memory_mb": memory_mb,
                "driver": driver_value,
                "available": model_name != "Unknown",
            }

        return {
            "model": platform.machine(),
            "memory_mb": 0,
            "driver": "Unknown",
            "available": False,
        }
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to collect GPU info: %s", exc)
        return {"model": "Unknown", "memory_mb": 0, "driver": "Unknown", "available": False}


def get_battery_info() -> dict[str, Any]:
    """Return battery information when available."""

    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return {"available": False, "percent": 0, "plugged": False, "remaining_hours": 0.0}

        secs_left = getattr(battery, "secsleft", None)
        remaining_hours = 0.0
        if secs_left is not None and secs_left >= 0:
            remaining_hours = round(secs_left / 3600, 2)

        return {
            "available": True,
            "percent": int(battery.percent),
            "plugged": bool(battery.power_plugged),
            "remaining_hours": remaining_hours,
        }
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to collect battery info: %s", exc)
        return {"available": False, "percent": 0, "plugged": False, "remaining_hours": 0.0}


def get_temperature_info() -> dict[str, Any]:
    """Return available temperature readings when supported by the system."""

    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return {"available": False, "readings": []}

        readings = []
        for name, entries in temps.items():
            if not entries:
                continue
            for reading in entries:
                current = reading.current
                high = reading.high
                readings.append(
                    {
                        "name": name,
                        "current": round(current, 2) if isinstance(current, (int, float)) else None,
                        "high": round(high, 2) if isinstance(high, (int, float)) else None,
                    }
                )

        return {"available": bool(readings), "readings": readings}
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to collect temperature info: %s", exc)
        return {"available": False, "readings": []}
