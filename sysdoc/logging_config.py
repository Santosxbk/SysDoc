"""Logging configuration for SysDoc."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any


def configure_logging(log_level: str = "INFO") -> None:
    """Configure application-wide logging with console and file handlers."""

    try:
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "sysdoc.log"

        logging.basicConfig(
            level=getattr(logging, log_level.upper(), logging.INFO),
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )
    except Exception as exc:  # pragma: no cover - defensive logging
        logging.getLogger(__name__).exception("Unable to configure logging: %s", exc)
