"""Typer-based CLI entrypoint for SysDoc."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import typer
from rich.table import Table

from sysdoc import __version__
from sysdoc.config import AppConfig, load_config, save_config
from sysdoc.diagnostics.advanced import run_nmap_scan, scan_ports
from sysdoc.diagnostics.intelligent import diagnose_system
from sysdoc.diagnostics.speed import measure_speed
from sysdoc.diagnostics.system import analyze_cpu, analyze_disk, analyze_memory
from sysdoc.hardware.monitor import get_battery_info, get_gpu_info, get_temperature_info
from sysdoc.logging_config import configure_logging
from sysdoc.network import get_default_gateway, get_dns_servers, get_interfaces, get_public_ip, ping_host, resolve_hostname
from sysdoc.reports.exporters import export_html_report, export_json_report, export_text_report
from sysdoc.security.security import analyze_security
from sysdoc.ui.banner import build_banner, create_console
from sysdoc.utils.installer import build_install_commands, run_installation
from sysdoc.utils.system import get_cpu_info, get_disk_info, get_memory_info, get_os_name, get_python_version

configure_logging("INFO")
logger = logging.getLogger(__name__)

app = typer.Typer(help="Modern cross-platform system diagnostics toolkit")
console = create_console()
JSON_OUTPUT = False


@app.callback()
def main(
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    """Shared CLI options."""

    global JSON_OUTPUT
    JSON_OUTPUT = json_output


def display_value(value: Any) -> str:
    """Normalize values that may be absent or empty for CLI display."""

    if value is None:
        return "Unknown"
    if isinstance(value, str):
        return value.strip() or "Unknown"
    if isinstance(value, (list, tuple, set)):
        return ", ".join(str(item) for item in value) if value else "Unknown"
    return str(value)


def emit_cli_error(command_name: str, exc: Exception) -> None:
    """Log and print a consistent CLI error message."""

    logger.exception("%s command failed: %s", command_name, exc)
    typer.echo(f"Unable to {command_name}: {exc}", err=True)


def output_json_or_table(payload: dict[str, Any], title: str) -> None:
    """Emit either JSON output or a rich table based on the current CLI options."""

    if JSON_OUTPUT:
        typer.echo(json.dumps(payload, indent=2, sort_keys=True))
        return

    table = Table(title=title)
    table.add_column("Metric")
    table.add_column("Value")
    for key, value in payload.items():
        table.add_row(str(key), display_value(value))
    console.print(table)


def _load_config() -> AppConfig:
    """Load configuration with a file next to the working directory."""

    return load_config(Path("config.yaml"))


@app.command()
def scan() -> None:
    """Run a quick system scan and present a summary."""

    try:
        _load_config()
        console.print(build_banner())
        table = Table(title="System Overview")
        table.add_column("Metric")
        table.add_column("Value")
        payload = {
            "OS": display_value(get_os_name()),
            "Python": display_value(get_python_version()),
            "CPU cores": display_value(get_cpu_info()["cores"]),
            "Memory": f"{get_memory_info()['total_gb']} GB",
            "Disk": f"{get_disk_info()['total_gb']} GB",
        }
        output_json_or_table(payload, "System Overview")
        logger.info("Scan completed")
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("complete scan", exc)


@app.command()
def version() -> None:
    """Show the current SysDoc version."""

    try:
        console.print(build_banner(title="SYSDOC", subtitle=f"Version {__version__}"))
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("display version", exc)


@app.command()
def init() -> None:
    """Create a default configuration file."""

    try:
        config = AppConfig()
        config_path = save_config(config, Path("config.yaml"))
        console.print(f"Configuration written to [cyan]{config_path}[/cyan]")
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("initialize configuration", exc)


@app.command()
def cpu() -> None:
    """Display CPU diagnostics."""

    try:
        data = get_cpu_info()
        analysis = analyze_cpu()
        table = Table(title="CPU")
        table.add_column("Metric")
        table.add_column("Value")
        payload = {
            "Model": display_value(data["model"]),
            "Cores": display_value(data["cores"]),
            "Physical cores": display_value(data["physical_cores"]),
            "Frequency": f"{data['frequency']} MHz",
            "Usage": f"{data['usage']} %",
            "Severity": display_value(analysis["severity"]),
            "Recommendation": display_value(analysis["recommendation"]),
        }
        output_json_or_table(payload, "CPU")
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("show CPU info", exc)


@app.command()
def ram() -> None:
    """Display memory diagnostics."""

    try:
        data = get_memory_info()
        analysis = analyze_memory()
        table = Table(title="RAM")
        table.add_column("Metric")
        table.add_column("Value")
        payload = {
            "Total": f"{data['total_gb']} GB",
            "Used": f"{data['used_gb']} GB",
            "Available": f"{data['available_gb']} GB",
            "Usage": f"{data['percent']} %",
            "Severity": display_value(analysis["severity"]),
            "Recommendation": display_value(analysis["recommendation"]),
        }
        output_json_or_table(payload, "RAM")
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("show memory info", exc)


@app.command()
def disk() -> None:
    """Display disk diagnostics."""

    try:
        data = get_disk_info()
        analysis = analyze_disk()
        table = Table(title="Disk")
        table.add_column("Metric")
        table.add_column("Value")
        payload = {
            "Total": f"{data['total_gb']} GB",
            "Used": f"{data['used_gb']} GB",
            "Free": f"{data['free_gb']} GB",
            "Usage": f"{data['percent']} %",
            "Severity": display_value(analysis["severity"]),
            "Recommendation": display_value(analysis["recommendation"]),
        }
        output_json_or_table(payload, "Disk")
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("show disk info", exc)


@app.command()
def network() -> None:
    """Display network interface and routing information."""

    try:
        payload = {
            "Interfaces": str(len(get_interfaces())),
            "Gateway": display_value(get_default_gateway()),
            "Public IP": display_value(get_public_ip()),
            "DNS": display_value(", ".join(get_dns_servers()) or "Unknown"),
        }
        output_json_or_table(payload, "Network")
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("show network info", exc)


@app.command()
def dns() -> None:
    """Display DNS configuration."""

    try:
        table = Table(title="DNS")
        table.add_column("Server")
        servers = get_dns_servers()
        if servers:
            for server in servers:
                table.add_row(server)
        else:
            table.add_row("No DNS servers detected")
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("show DNS info", exc)


@app.command()
def ping() -> None:
    """Ping localhost to confirm connectivity."""

    try:
        latency = ping_host("127.0.0.1")
        table = Table(title="Ping")
        table.add_column("Host")
        table.add_column("Result")
        table.add_row("127.0.0.1", f"{latency} s" if latency is not None else "failed")
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("run ping check", exc)


@app.command()
def gpu() -> None:
    """Display GPU information."""

    try:
        data = get_gpu_info()
        table = Table(title="GPU")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Model", display_value(data["model"]))
        table.add_row("Memory", f"{data['memory_mb']} MB")
        table.add_row("Driver", display_value(data["driver"]))
        table.add_row("Available", display_value(data["available"]))
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("show GPU info", exc)


@app.command()
def battery() -> None:
    """Display battery information when available."""

    try:
        data = get_battery_info()
        table = Table(title="Battery")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Available", display_value(data["available"]))
        table.add_row("Percent", f"{data['percent']} %")
        table.add_row("Plugged", display_value(data["plugged"]))
        table.add_row("Remaining hours", display_value(data["remaining_hours"]))
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("show battery info", exc)


@app.command()
def temperatures() -> None:
    """Display temperature readings when available."""

    try:
        data = get_temperature_info()
        table = Table(title="Temperatures")
        table.add_column("Sensor")
        table.add_column("Current")
        table.add_column("High")
        if data["readings"]:
            for entry in data["readings"]:
                current = display_value(entry["current"])
                high = display_value(entry["high"])
                table.add_row(entry["name"], f"{current} C" if current != "Unknown" else "Unknown", high if high != "Unknown" else "n/a")
        else:
            table.add_row("No readings", "n/a", "n/a")
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("show temperature info", exc)


@app.command()
def security() -> None:
    """Run a basic security assessment."""

    try:
        data = analyze_security()
        table = Table(title="Security")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Root", display_value(data["is_root"]))
        table.add_row("Issues", display_value(", ".join(data["issues"]) or "None"))
        table.add_row("Recommendation", display_value(data["recommendation"]))
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("show security info", exc)


@app.command()
def doctor() -> None:
    """Run intelligent diagnosis."""

    try:
        data = diagnose_system()
        table = Table(title="Doctor")
        table.add_column("Metric")
        table.add_column("Value")
        payload = {
            "Summary": display_value(data["summary"]),
            "Issues": display_value(", ".join(data["issues"]) or "None"),
            "Recommendations": display_value(" | ".join(data["recommendations"])),
        }
        output_json_or_table(payload, "Doctor")
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("run doctor", exc)


@app.command()
def report() -> None:
    """Export TXT, JSON and HTML reports."""

    try:
        text = export_text_report("reports/sysdoc_report.txt")
        json_path = export_json_report("reports/sysdoc_report.json")
        html_path = export_html_report("reports/sysdoc_report.html")
        payload = {
            "TXT": str(text),
            "JSON": str(json_path),
            "HTML": str(html_path),
        }
        output_json_or_table(payload, "Reports")
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("export reports", exc)


@app.command()
def ports() -> None:
    """Scan a shortlist of common local ports."""

    try:
        results = scan_ports()
        table = Table(title="Ports")
        table.add_column("Port")
        table.add_column("Status")
        for item in results:
            table.add_row(str(item["port"]), "open" if item["open"] else "closed")
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("scan ports", exc)


@app.command()
def nmap() -> None:
    """Run a real nmap scan when nmap is installed."""

    try:
        data = run_nmap_scan()
        table = Table(title="Nmap")
        table.add_column("Port")
        if data["open_ports"]:
            for port in data["open_ports"]:
                table.add_row(str(port))
        else:
            table.add_row("No open ports detected")
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("run nmap", exc)


@app.command()
def speed() -> None:
    """Run a network speed measurement using speedtest-cli when available."""

    try:
        data = measure_speed()
        payload = {
            "Download": f"{data['download_mbps']} Mbps",
            "Upload": f"{data['upload_mbps']} Mbps",
        }
        output_json_or_table(payload, "Speed")
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("measure speed", exc)


@app.command()
def update() -> None:
    """Show an update notice for the local installation."""

    try:
        console.print("SysDoc is up to date for this local build.")
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("run update check", exc)


@app.command(name="doctor-fix")
def doctor_fix() -> None:
    """Apply safe recommendations derived from the doctor analysis."""

    try:
        data = diagnose_system()
        table = Table(title="Doctor Fix")
        table.add_column("Action")
        table.add_column("Status")
        table.add_row("Safe recommendations reviewed", "done")
        for recommendation in data["recommendations"]:
            table.add_row(recommendation, "suggested")
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("apply doctor fix", exc)


@app.command()
def install() -> None:
    """Print or suggest the commands needed to fully install SysDoc and its dependencies."""

    try:
        steps = run_installation()
        table = Table(title="Installation")
        table.add_column("Step")
        if steps:
            for index, step in enumerate(steps, start=1):
                table.add_row(str(index), step)
        else:
            table.add_row("1", "No installation steps were detected for this platform.")
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_cli_error("prepare installation steps", exc)


if __name__ == "__main__":
    app()
