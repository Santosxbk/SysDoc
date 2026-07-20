"""Basic security scanning helpers for SysDoc."""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


def analyze_security() -> dict[str, Any]:
    """Return a basic security summary without performing destructive actions."""

    try:
        is_root = os.geteuid() == 0 if hasattr(os, "geteuid") else False
        return {
            "is_root": is_root,
            "issues": [],
            "recommendation": "No immediate security issues detected." if not is_root else "Running as root increases risk; prefer a limited user account.",
        }
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to analyze security posture: %s", exc)
        return {"is_root": False, "issues": ["Unable to perform security analysis."], "recommendation": "Unable to analyze security."}
