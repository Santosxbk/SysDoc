"""Network diagnostics helpers for SysDoc."""

from .network import get_default_gateway, get_dns_servers, get_interfaces, get_public_ip, ping_host, resolve_hostname

__all__ = ["get_default_gateway", "get_dns_servers", "get_interfaces", "get_public_ip", "ping_host", "resolve_hostname"]
