from sysdoc.diagnostics.speed import measure_speed, parse_speedtest_output


def test_measure_speed_returns_values() -> None:
    result = measure_speed()

    assert isinstance(result["download_mbps"], float)
    assert isinstance(result["upload_mbps"], float)


def test_parse_speedtest_output_parses_mbps() -> None:
    sample = "Ping: 12.3 ms\nDownload: 123.45 Mbit/s\nUpload: 67.89 Mbit/s\n"
    parsed = parse_speedtest_output(sample)

    assert parsed["download_mbps"] == 123.45
    assert parsed["upload_mbps"] == 67.89
