from pathlib import Path

from sysdoc.reports.exporters import export_html_report, export_json_report, export_text_report


def test_reports_are_written(tmp_path: Path) -> None:
    text_path = tmp_path / "report.txt"
    json_path = tmp_path / "report.json"
    html_path = tmp_path / "report.html"

    export_text_report(text_path)
    export_json_report(json_path)
    export_html_report(html_path)

    assert text_path.exists()
    assert json_path.exists()
    assert html_path.exists()
