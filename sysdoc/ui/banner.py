"""Banner and console rendering helpers for SysDoc."""

from __future__ import annotations

import logging
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

logger = logging.getLogger(__name__)


def build_banner(title: str = "SYSDOC", subtitle: str = "System Diagnostics Toolkit") -> Panel:
    """Create a rich panel banner for the CLI."""

    try:
        text = Text()
        text.append(title, style="bold cyan")
        text.append("\n")
        text.append(subtitle, style="white")
        return Panel(text, border_style="cyan", padding=(1, 2))
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to render banner: %s", exc)
        return Panel("SysDoc", border_style="red")


def create_console() -> Console:
    """Create a configured rich console instance."""

    try:
        return Console(highlight=False, soft_wrap=True)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to create console: %s", exc)
        return Console()
