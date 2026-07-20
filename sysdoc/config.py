"""Application configuration helpers for SysDoc."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class AppConfig:
    """Runtime configuration for the SysDoc CLI."""

    colors: bool = True
    language: str = "pt"
    theme: str = "dark"
    log_level: str = "INFO"
    timeout: int = 5


def load_config(path: str | Path | None = None) -> AppConfig:
    """Load configuration from disk, returning defaults on missing files."""

    config_path = Path(path or "config.yaml")
    try:
        if not config_path.exists():
            logger.info("Using default configuration because %s does not exist", config_path)
            return AppConfig()

        with config_path.open("r", encoding="utf-8") as handle:
            data: dict[str, Any] = yaml.safe_load(handle) or {}

        return AppConfig(
            colors=bool(data.get("colors", True)),
            language=str(data.get("language", "pt")),
            theme=str(data.get("theme", "dark")),
            log_level=str(data.get("log_level", "INFO")),
            timeout=int(data.get("timeout", 5)),
        )
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to load configuration from %s: %s", config_path, exc)
        return AppConfig()


def save_config(config: AppConfig, path: str | Path | None = None) -> Path:
    """Persist configuration to disk."""

    config_path = Path(path or "config.yaml")
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(
                {
                    "colors": config.colors,
                    "language": config.language,
                    "theme": config.theme,
                    "log_level": config.log_level,
                    "timeout": config.timeout,
                },
                handle,
                sort_keys=False,
            )
        logger.info("Configuration saved to %s", config_path)
        return config_path
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to save configuration to %s: %s", config_path, exc)
        raise
