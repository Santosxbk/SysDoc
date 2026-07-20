"""System information helpers for SysDoc."""

from __future__ import annotations

import logging
import platform
import shutil
import socket
from pathlib import Path
from typing import Any

import psutil

logger = logging.getLogger(__name__)


def get_os_name() -> str:
    """Return a human-friendly operating system name."""

    try:
        return platform.system() or "Unknown"
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to determine operating system: %s", exc)
        return "Unknown"


def get_cpu_info() -> dict[str, Any]:
    """Collect CPU information in a stable dictionary format."""

    try:
        return {
            "model": platform.processor() or platform.machine(),
            "cores": psutil.cpu_count(logical=True) or 1,
            "physical_cores": psutil.cpu_count(logical=False) or 1,
            "frequency": round(psutil.cpu_freq().current, 2) if psutil.cpu_freq() else 0.0,
            "usage": round(psutil.cpu_percent(interval=None), 2),
        }
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to collect CPU info: %s", exc)
        return {"model": "Unknown", "cores": 1, "physical_cores": 1, "frequency": 0.0, "usage": 0.0}


def get_memory_info() -> dict[str, Any]:
    """Collect memory information in gigabytes."""

    try:
        memory = psutil.virtual_memory()
        return {
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "used_gb": round(memory.used / (1024**3), 2),
            "percent": round(memory.percent, 2),
        }
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to collect memory info: %s", exc)
        return {"total_gb": 0.0, "available_gb": 0.0, "used_gb": 0.0, "percent": 0.0}


def get_disk_info() -> dict[str, Any]:
    """Collect disk information for the root partition."""

    try:
        disk = psutil.disk_usage(Path("/").as_posix())
        return {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percent": round(disk.percent, 2),
        }
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to collect disk info: %s", exc)
        return {"total_gb": 0.0, "used_gb": 0.0, "free_gb": 0.0, "percent": 0.0}


def get_hostname() -> str:
    """Return the current host name."""

    try:
        return socket.gethostname()
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to determine hostname: %s", exc)
        return "Unknown"


def get_python_version() -> str:
    """Return the running Python version."""

    try:
        return platform.python_version()
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to determine Python version: %s", exc)
        return "Unknown"


def get_available_disk_space(path: str | Path | None = None) -> float:
    """Return free disk space in gigabytes for a path."""

    target = Path(path or "/")
    try:
        usage = shutil.disk_usage(target)
        return round(usage.free / (1024**3), 2)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to get disk space for %s: %s", target, exc)
        return 0.0
