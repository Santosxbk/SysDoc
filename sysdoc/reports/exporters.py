"""Text, JSON and HTML report exporters for SysDoc."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from jinja2 import Template
except ModuleNotFoundError:  # pragma: no cover - optional dependency fallback
    Template = None

from sysdoc.diagnostics.system import analyze_cpu, analyze_disk, analyze_memory
from sysdoc.hardware.monitor import get_battery_info, get_gpu_info, get_temperature_info
from sysdoc.network import get_default_gateway, get_dns_servers, get_interfaces, get_public_ip
from sysdoc.utils.system import get_cpu_info, get_disk_info, get_memory_info, get_os_name, get_python_version

logger = logging.getLogger(__name__)


def export_text_report(path: str | Path | None = None) -> Path:
    """Export a plain text report to disk."""

    report_path = Path(path or "reports/sysdoc_report.txt")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        lines = [
            "SysDoc Report",
            "============",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            f"OS: {get_os_name()}",
            f"Python: {get_python_version()}",
            f"CPU: {get_cpu_info()['usage']}%",
            f"RAM: {get_memory_info()['percent']}%",
            f"Disk: {get_disk_info()['percent']}%",
            f"Gateway: {get_default_gateway() or 'Unknown'}",
            f"Public IP: {get_public_ip() or 'Unknown'}",
        ]
        report_path.write_text("\n".join(lines), encoding="utf-8")
        logger.info("Text report written to %s", report_path)
        return report_path
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to export text report: %s", exc)
        raise


def export_json_report(path: str | Path | None = None) -> Path:
    """Export a JSON report to disk."""

    report_path = Path(path or "reports/sysdoc_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "os": get_os_name(),
            "python": get_python_version(),
            "cpu": analyze_cpu(),
            "memory": analyze_memory(),
            "disk": analyze_disk(),
            "gpu": get_gpu_info(),
            "battery": get_battery_info(),
            "temperatures": get_temperature_info(),
            "network": {"gateway": get_default_gateway(), "dns": get_dns_servers(), "public_ip": get_public_ip()},
        }
        report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        logger.info("JSON report written to %s", report_path)
        return report_path
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to export JSON report: %s", exc)
        raise


def export_html_report(path: str | Path | None = None) -> Path:
    """Export an HTML report to disk."""

    report_path = Path(path or "reports/sysdoc_report.html")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        generated_at = datetime.now(timezone.utc).isoformat()
        cpu = analyze_cpu()
        memory = analyze_memory()
        disk = analyze_disk()

        if Template is not None:
            rendered = Template("""
            <html>
              <head><title>SysDoc Report</title></head>
              <body>
                <h1>SysDoc Report</h1>
                <p>Generated: {{ generated_at }}</p>
                <h2>System</h2>
                <ul>
                  <li>OS: {{ os }}</li>
                  <li>Python: {{ python }}</li>
                </ul>
                <h2>Diagnostics</h2>
                <ul>
                  <li>CPU: {{ cpu.severity }} - {{ cpu.recommendation }}</li>
                  <li>Memory: {{ memory.severity }} - {{ memory.recommendation }}</li>
                  <li>Disk: {{ disk.severity }} - {{ disk.recommendation }}</li>
                </ul>
              </body>
            </html>
            """).render(
                generated_at=generated_at,
                os=get_os_name(),
                python=get_python_version(),
                cpu=cpu,
                memory=memory,
                disk=disk,
            )
        else:
            rendered = (
                "<html><head><title>SysDoc Report</title></head><body>"
                f"<h1>SysDoc Report</h1><p>Generated: {generated_at}</p>"
                f"<h2>System</h2><ul><li>OS: {get_os_name()}</li><li>Python: {get_python_version()}</li></ul>"
                f"<h2>Diagnostics</h2><ul>"
                f"<li>CPU: {cpu['severity']} - {cpu['recommendation']}</li>"
                f"<li>Memory: {memory['severity']} - {memory['recommendation']}</li>"
                f"<li>Disk: {disk['severity']} - {disk['recommendation']}</li>"
                "</ul></body></html>"
            )

        report_path.write_text(rendered, encoding="utf-8")
        logger.info("HTML report written to %s", report_path)
        return report_path
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Unable to export HTML report: %s", exc)
        raise
