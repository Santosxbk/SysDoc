"""Network diagnostics helpers for SysDoc."""

from __future__ import annotations

import logging
import socket
from typing import Any

import psutil
import requests
from dns import resolver
from ping3 import ping

logger = logging.getLogger(__name__)


def get_interfaces() -> list[dict[str, Any]]:
    """Return a lightweight list of network interfaces with addresses and status."""

    try:
        interfaces: list[dict[str, Any]] = []
        for name, data in psutil.net_if_addrs().items():
            addresses = [item.address for item in data if item.address and not item.address.startswith("127.")]
            interfaces.append({"name": name, "addresses": addresses, "is_up": name in psutil.net_if_stats() and psutil.net_if_stats()[name].isup})
        return interfaces
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to collect network interfaces: %s", exc)
        return []


def get_default_gateway() -> str | None:
    """Return the default gateway address when available."""

    try:
        gateways = psutil.net_if_addrs().get("eth0") or psutil.net_if_addrs().get("en0")
        if gateways:
            return next((address.address for address in gateways if address.family == socket.AF_INET), None)
        return None
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to determine default gateway: %s", exc)
        return None


def get_dns_servers() -> list[str]:
    """Return configured DNS servers from the local resolver."""

    try:
        return [item for item in resolver.Resolver().nameservers if item]
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to resolve DNS servers: %s", exc)
        return []


def resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to IP addresses using the system resolver."""

    try:
        answers = resolver.resolve(hostname, "A")
        return [str(answer) for answer in answers]
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to resolve hostname %s: %s", hostname, exc)
        return []


def ping_host(hostname: str) -> float | None:
    """Ping a host and return the round-trip time in seconds."""

    try:
        response = ping(hostname, timeout=2)
        return float(response) if response is not None else None
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to ping host %s: %s", hostname, exc)
        return None


def get_public_ip() -> str | None:
    """Return the public IP using a public HTTP endpoint."""

    try:
        response = requests.get("https://api.ipify.org", timeout=3)
        response.raise_for_status()
        return response.text.strip()
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to determine public IP: %s", exc)
        return None
