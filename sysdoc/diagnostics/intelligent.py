"""Intelligent troubleshooting helpers for SysDoc."""

from __future__ import annotations

import logging
from typing import Any

from sysdoc.diagnostics.system import analyze_cpu, analyze_disk, analyze_memory

logger = logging.getLogger(__name__)


def diagnose_system() -> dict[str, Any]:
    """Create a consolidated diagnosis across CPU, memory and disk."""

    try:
        cpu = analyze_cpu()
        memory = analyze_memory()
        disk = analyze_disk()
        issues = []
        if cpu["severity"] == "high":
            issues.append("CPU usage is very high")
        if memory["severity"] == "high":
            issues.append("Memory usage is very high")
        if disk["severity"] == "high":
            issues.append("Disk space is critically low")
        return {
            "summary": "No critical issues detected." if not issues else "; ".join(issues),
            "issues": issues,
            "recommendations": [cpu["recommendation"], memory["recommendation"], disk["recommendation"]],
        }
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to produce intelligent diagnosis: %s", exc)
        return {"summary": "Unable to diagnose system.", "issues": ["diagnosis_failed"], "recommendations": []}
