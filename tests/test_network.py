import socket
from types import SimpleNamespace

from sysdoc.network import get_default_gateway, get_dns_servers, get_interfaces, ping_host, resolve_hostname


def test_network_helpers_return_expected_shapes() -> None:
    interfaces = get_interfaces()
    gateway = get_default_gateway()
    dns_servers = get_dns_servers()
    resolution = resolve_hostname("localhost")
    latency = ping_host("127.0.0.1")

    assert isinstance(interfaces, list)
    assert all(isinstance(item, dict) for item in interfaces)
    assert gateway is None or isinstance(gateway, str)
    assert isinstance(dns_servers, list)
    assert all(isinstance(item, str) for item in dns_servers)
    assert isinstance(resolution, list)
    assert all(isinstance(item, str) for item in resolution)
    assert latency is None or isinstance(latency, float)


def test_get_default_gateway_uses_linux_route_when_interface_name_is_not_eth0(monkeypatch) -> None:
    monkeypatch.setattr(
        "sysdoc.network.network.psutil.net_if_addrs",
        lambda: {"wlp2s0": [SimpleNamespace(address="192.168.0.12", family=socket.AF_INET)]},
    )
    monkeypatch.setattr(
        "sysdoc.network.network._read_default_gateway_from_proc",
        lambda: "192.168.0.1",
    )

    assert get_default_gateway() == "192.168.0.1"
