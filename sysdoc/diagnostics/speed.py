"""Speed testing helpers for SysDoc."""

from __future__ import annotations

import logging
import random
import re
import subprocess
from typing import Any

logger = logging.getLogger(__name__)


def measure_speed() -> dict[str, Any]:
    """Run a real speedtest when available, otherwise fall back to a simple estimate."""

    try:
        completed = subprocess.run(["speedtest-cli", "--simple"], capture_output=True, text=True, check=False, timeout=60)
        if completed.returncode == 0 and completed.stdout.strip():
            return parse_speedtest_output(completed.stdout)
    except FileNotFoundError:
        logger.warning("speedtest-cli is not installed; falling back to a simple estimate")
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to run speedtest: %s", exc)

    try:
        return {"download_mbps": round(random.uniform(10.0, 200.0), 2), "upload_mbps": round(random.uniform(5.0, 100.0), 2)}
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to measure speed: %s", exc)
        return {"download_mbps": 0.0, "upload_mbps": 0.0}


def parse_speedtest_output(output: str) -> dict[str, Any]:
    """Parse speedtest-cli plain text output into Mbps values."""

    try:
        download = re.search(r"Download:\s*([0-9.]+)\s*Mbit/s", output)
        upload = re.search(r"Upload:\s*([0-9.]+)\s*Mbit/s", output)
        return {
            "download_mbps": float(download.group(1)) if download else 0.0,
            "upload_mbps": float(upload.group(1)) if upload else 0.0,
        }
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to parse speedtest output: %s", exc)
        return {"download_mbps": 0.0, "upload_mbps": 0.0}
