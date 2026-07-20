"""Helpers to automate environment setup for SysDoc."""

from __future__ import annotations

import logging
import platform
import subprocess
import sys
from typing import Any

logger = logging.getLogger(__name__)


def detect_package_manager(os_name: str | None = None) -> str | None:
    """Detect the most suitable package manager for the host OS."""

    system = (os_name or platform.system()).lower()
    try:
        if system in {"linux", "linux2"}:
            if subprocess.run(["which", "apt-get"], capture_output=True, text=True, check=False).returncode == 0:
                return "apt"
            if subprocess.run(["which", "dnf"], capture_output=True, text=True, check=False).returncode == 0:
                return "dnf"
            if subprocess.run(["which", "pacman"], capture_output=True, text=True, check=False).returncode == 0:
                return "pacman"
        if system == "windows":
            return "winget"
        if system == "darwin":
            return "brew"
        return None
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to detect package manager: %s", exc)
        return None


def build_install_commands(os_name: str | None = None) -> list[str]:
    """Create the commands needed to install SysDoc dependencies and external tools."""

    manager = detect_package_manager(os_name)
    commands: list[str] = []
    if manager == "apt":
        commands.append("sudo apt-get update")
        commands.append("sudo apt-get install -y nmap speedtest-cli")
    elif manager == "dnf":
        commands.append("sudo dnf install -y nmap speedtest-cli")
    elif manager == "pacman":
        commands.append("sudo pacman -S --noconfirm nmap speedtest-cli")
    elif manager == "brew":
        commands.append("brew install nmap speedtest-cli")
    elif manager == "winget":
        commands.append("winget install -e --id Insecure.Nmap")
        commands.append("winget install -e --id Speedtest.net.Speedtest")

    commands.append(f"{sys.executable} -m pip install -r requirements.txt")
    return commands


def run_installation(os_name: str | None = None) -> list[str]:
    """Return the installation steps that should be executed for the current environment."""

    try:
        return build_install_commands(os_name)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to prepare installation steps: %s", exc)
        return []
