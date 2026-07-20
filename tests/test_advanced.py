from sysdoc.diagnostics.advanced import parse_nmap_output, scan_ports


def test_scan_ports_returns_results() -> None:
    results = scan_ports("127.0.0.1", [80])

    assert isinstance(results, list)
    assert all(isinstance(item, dict) for item in results)
    assert all("port" in item and "open" in item for item in results)


def test_parse_nmap_output_extracts_ports() -> None:
    sample = "Nmap scan report for localhost\n80/tcp open http\n443/tcp closed https\n"
    parsed = parse_nmap_output(sample)

    assert parsed["open_ports"] == [80]
