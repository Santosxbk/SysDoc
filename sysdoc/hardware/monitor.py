"""Hardware monitoring helpers for GPU, battery and temperature data."""

from __future__ import annotations

import logging
import platform
from typing import Any

import psutil

logger = logging.getLogger(__name__)


def get_gpu_info() -> dict[str, Any]:
    """Return a best-effort GPU summary."""

    try:
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
        return {
            "available": True,
            "percent": int(battery.percent),
            "plugged": bool(battery.power_plugged),
            "remaining_hours": round(battery.secsleft / 3600, 2) if battery.secsleft >= 0 else 0.0,
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
            if entries:
                reading = entries[0]
                readings.append({"name": name, "current": round(reading.current, 2), "high": round(reading.high, 2) if reading.high else None})
        return {"available": True, "readings": readings}
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to collect temperature info: %s", exc)
        return {"available": False, "readings": []}
