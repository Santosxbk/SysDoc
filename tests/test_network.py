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
