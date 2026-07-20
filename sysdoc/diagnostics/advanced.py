"""Advanced diagnostics helpers for ports and uptime-style checks."""

from __future__ import annotations

import logging
import re
import socket
import subprocess
from typing import Any

logger = logging.getLogger(__name__)


def scan_ports(host: str = "127.0.0.1", ports: list[int] | None = None) -> list[dict[str, Any]]:
    """Scan a shortlist of local ports and report which ones are open."""

    candidates = ports or [22, 80, 443]
    results: list[dict[str, Any]] = []
    for port in candidates:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                sock.connect((host, port))
                results.append({"port": port, "open": True})
        except OSError:
            results.append({"port": port, "open": False})
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.exception("Unable to scan port %s: %s", port, exc)
            results.append({"port": port, "open": False})
    return results


def run_nmap_scan(target: str = "127.0.0.1") -> dict[str, Any]:
    """Run nmap if it is available and return parsed results."""

    try:
        completed = subprocess.run(["nmap", "-Pn", target], capture_output=True, text=True, check=False, timeout=20)
        if completed.returncode not in {0, 1}:
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "nmap failed")
        return parse_nmap_output(completed.stdout)
    except FileNotFoundError:
        logger.warning("nmap is not installed; returning an empty result set")
        return {"target": target, "open_ports": [], "raw_output": ""}
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to run nmap scan: %s", exc)
        return {"target": target, "open_ports": [], "raw_output": ""}


def parse_nmap_output(output: str) -> dict[str, Any]:
    """Parse nmap text output and extract open TCP ports."""

    try:
        open_ports: list[int] = []
        for line in output.splitlines():
            match = re.match(r"^(\d+)/tcp\s+(open|open|filtered|closed)\s+", line)
            if match:
                port = int(match.group(1))
                if match.group(2) == "open":
                    open_ports.append(port)
        return {"target": "unknown", "open_ports": open_ports, "raw_output": output}
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to parse nmap output: %s", exc)
        return {"target": "unknown", "open_ports": [], "raw_output": output}
