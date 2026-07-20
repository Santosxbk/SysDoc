"""System diagnostics and recommendations for CPU, RAM and disk."""

from __future__ import annotations

import logging
from typing import Any

from sysdoc.utils.system import get_cpu_info, get_disk_info, get_memory_info

logger = logging.getLogger(__name__)


def analyze_cpu() -> dict[str, Any]:
    """Analyze CPU usage and produce a simple recommendation."""

    try:
        data = get_cpu_info()
        usage = data["usage"]
        if usage >= 90:
            severity = "high"
            recommendation = "High CPU usage detected. Close heavy applications or check for background processes."
        elif usage >= 70:
            severity = "medium"
            recommendation = "CPU usage is elevated. Review running tasks and consider reducing load."
        else:
            severity = "low"
            recommendation = "CPU usage is within normal bounds."
        return {"usage": usage, "severity": severity, "recommendation": recommendation}
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to analyze CPU: %s", exc)
        return {"usage": 0.0, "severity": "unknown", "recommendation": "Unable to analyze CPU."}


def analyze_memory() -> dict[str, Any]:
    """Analyze memory pressure and produce a simple recommendation."""

    try:
        data = get_memory_info()
        percent = data["percent"]
        if percent >= 90:
            severity = "high"
            recommendation = "Memory pressure is very high. Close unused applications and free up memory."
        elif percent >= 70:
            severity = "medium"
            recommendation = "Memory usage is elevated. Consider closing resource-heavy applications."
        else:
            severity = "low"
            recommendation = "Memory usage appears healthy."
        return {"percent": percent, "severity": severity, "recommendation": recommendation}
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to analyze memory: %s", exc)
        return {"percent": 0.0, "severity": "unknown", "recommendation": "Unable to analyze memory."}


def analyze_disk() -> dict[str, Any]:
    """Analyze disk space usage and produce a simple recommendation."""

    try:
        data = get_disk_info()
        percent = data["percent"]
        if percent >= 90:
            severity = "high"
            recommendation = "Disk space is critically low. Remove unnecessary files or expand storage."
        elif percent >= 70:
            severity = "medium"
            recommendation = "Disk usage is high. Clean temporary files and archives."
        else:
            severity = "low"
            recommendation = "Disk usage is acceptable."
        return {"percent": percent, "severity": severity, "recommendation": recommendation}
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to analyze disk: %s", exc)
        return {"percent": 0.0, "severity": "unknown", "recommendation": "Unable to analyze disk."}
