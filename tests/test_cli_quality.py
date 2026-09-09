from sysdoc import __version__
from sysdoc.cli.app import display_value, emit_cli_error


def test_version_is_available() -> None:
    assert isinstance(__version__, str)
    assert __version__


def test_display_value_handles_missing_values() -> None:
    assert display_value(None) == "Unknown"
    assert display_value("") == "Unknown"
    assert display_value("ok") == "ok"


def test_emit_cli_error_writes_to_stderr(capsys) -> None:
    emit_cli_error("scan", RuntimeError("boom"))

    captured = capsys.readouterr()
    assert "scan" in captured.err
    assert "boom" in captured.err
