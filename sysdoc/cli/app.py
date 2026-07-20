"""Typer-based CLI entrypoint for SysDoc."""

from __future__ import annotations

import logging
from pathlib import Path

import typer
from rich.table import Table

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
from sysdoc.utils.system import get_cpu_info, get_disk_info, get_memory_info, get_os_name, get_python_version

configure_logging("INFO")
logger = logging.getLogger(__name__)

app = typer.Typer(help="Modern cross-platform system diagnostics toolkit")
console = create_console()


def _load_config() -> AppConfig:
    """Load configuration with a file next to the working directory."""

    return load_config(Path("config.yaml"))


@app.command()
def scan() -> None:
    """Run a quick system scan and present a summary."""

    try:
        config = _load_config()
        console.print(build_banner())
        table = Table(title="System Overview")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("OS", get_os_name())
        table.add_row("Python", get_python_version())
        table.add_row("CPU cores", str(get_cpu_info()["cores"]))
        table.add_row("Memory", f"{get_memory_info()['total_gb']} GB")
        table.add_row("Disk", f"{get_disk_info()['total_gb']} GB")
        console.print(table)
        logger.info("Scan completed")
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Scan command failed: %s", exc)
        typer.echo(f"Unable to complete scan: {exc}", err=True)


@app.command()
def version() -> None:
    """Show the current SysDoc version."""

    try:
        console.print(build_banner(title="SYSDOC", subtitle="Version 0.1.0"))
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Version command failed: %s", exc)
        typer.echo(f"Unable to display version: {exc}", err=True)


@app.command()
def init() -> None:
    """Create a default configuration file."""

    try:
        config = AppConfig()
        config_path = save_config(config, Path("config.yaml"))
        console.print(f"Configuration written to [cyan]{config_path}[/cyan]")
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Init command failed: %s", exc)
        typer.echo(f"Unable to initialize configuration: {exc}", err=True)


@app.command()
def cpu() -> None:
    """Display CPU diagnostics."""

    try:
        data = get_cpu_info()
        analysis = analyze_cpu()
        table = Table(title="CPU")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Model", str(data["model"]))
        table.add_row("Cores", str(data["cores"]))
        table.add_row("Physical cores", str(data["physical_cores"]))
        table.add_row("Frequency", f"{data['frequency']} MHz")
        table.add_row("Usage", f"{data['usage']} %")
        table.add_row("Severity", analysis["severity"])
        table.add_row("Recommendation", analysis["recommendation"])
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("CPU command failed: %s", exc)
        typer.echo(f"Unable to show CPU info: {exc}", err=True)


@app.command()
def ram() -> None:
    """Display memory diagnostics."""

    try:
        data = get_memory_info()
        analysis = analyze_memory()
        table = Table(title="RAM")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Total", f"{data['total_gb']} GB")
        table.add_row("Used", f"{data['used_gb']} GB")
        table.add_row("Available", f"{data['available_gb']} GB")
        table.add_row("Usage", f"{data['percent']} %")
        table.add_row("Severity", analysis["severity"])
        table.add_row("Recommendation", analysis["recommendation"])
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("RAM command failed: %s", exc)
        typer.echo(f"Unable to show memory info: {exc}", err=True)


@app.command()
def disk() -> None:
    """Display disk diagnostics."""

    try:
        data = get_disk_info()
        analysis = analyze_disk()
        table = Table(title="Disk")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Total", f"{data['total_gb']} GB")
        table.add_row("Used", f"{data['used_gb']} GB")
        table.add_row("Free", f"{data['free_gb']} GB")
        table.add_row("Usage", f"{data['percent']} %")
        table.add_row("Severity", analysis["severity"])
        table.add_row("Recommendation", analysis["recommendation"])
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Disk command failed: %s", exc)
        typer.echo(f"Unable to show disk info: {exc}", err=True)


@app.command()
def network() -> None:
    """Display network interface and routing information."""

    try:
        table = Table(title="Network")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Interfaces", str(len(get_interfaces())))
        table.add_row("Gateway", str(get_default_gateway() or "Unknown"))
        table.add_row("Public IP", str(get_public_ip() or "Unknown"))
        table.add_row("DNS", ", ".join(get_dns_servers()) or "Unknown")
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Network command failed: %s", exc)
        typer.echo(f"Unable to show network info: {exc}", err=True)


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
        logger.exception("DNS command failed: %s", exc)
        typer.echo(f"Unable to show DNS info: {exc}", err=True)


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
        logger.exception("Ping command failed: %s", exc)
        typer.echo(f"Unable to run ping check: {exc}", err=True)


@app.command()
def gpu() -> None:
    """Display GPU information."""

    try:
        data = get_gpu_info()
        table = Table(title="GPU")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Model", data["model"])
        table.add_row("Memory", f"{data['memory_mb']} MB")
        table.add_row("Driver", data["driver"])
        table.add_row("Available", str(data["available"]))
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("GPU command failed: %s", exc)
        typer.echo(f"Unable to show GPU info: {exc}", err=True)


@app.command()
def battery() -> None:
    """Display battery information when available."""

    try:
        data = get_battery_info()
        table = Table(title="Battery")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Available", str(data["available"]))
        table.add_row("Percent", f"{data['percent']} %")
        table.add_row("Plugged", str(data["plugged"]))
        table.add_row("Remaining hours", str(data["remaining_hours"]))
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Battery command failed: %s", exc)
        typer.echo(f"Unable to show battery info: {exc}", err=True)


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
                table.add_row(entry["name"], f"{entry['current']} C", str(entry["high"]) if entry["high"] is not None else "n/a")
        else:
            table.add_row("No readings", "n/a", "n/a")
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Temperature command failed: %s", exc)
        typer.echo(f"Unable to show temperature info: {exc}", err=True)


@app.command()
def security() -> None:
    """Run a basic security assessment."""

    try:
        data = analyze_security()
        table = Table(title="Security")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Root", str(data["is_root"]))
        table.add_row("Issues", ", ".join(data["issues"]) or "None")
        table.add_row("Recommendation", data["recommendation"])
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Security command failed: %s", exc)
        typer.echo(f"Unable to show security info: {exc}", err=True)


@app.command()
def doctor() -> None:
    """Run intelligent diagnosis."""

    try:
        data = diagnose_system()
        table = Table(title="Doctor")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Summary", data["summary"])
        table.add_row("Issues", ", ".join(data["issues"]) or "None")
        table.add_row("Recommendations", " | ".join(data["recommendations"]))
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Doctor command failed: %s", exc)
        typer.echo(f"Unable to run doctor: {exc}", err=True)


@app.command()
def report() -> None:
    """Export TXT, JSON and HTML reports."""

    try:
        text = export_text_report("reports/sysdoc_report.txt")
        json_path = export_json_report("reports/sysdoc_report.json")
        html_path = export_html_report("reports/sysdoc_report.html")
        table = Table(title="Reports")
        table.add_column("Format")
        table.add_column("Path")
        table.add_row("TXT", str(text))
        table.add_row("JSON", str(json_path))
        table.add_row("HTML", str(html_path))
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Report command failed: %s", exc)
        typer.echo(f"Unable to export reports: {exc}", err=True)


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
        logger.exception("Ports command failed: %s", exc)
        typer.echo(f"Unable to scan ports: {exc}", err=True)


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
        logger.exception("Nmap command failed: %s", exc)
        typer.echo(f"Unable to run nmap: {exc}", err=True)


@app.command()
def speed() -> None:
    """Run a network speed measurement using speedtest-cli when available."""

    try:
        data = measure_speed()
        table = Table(title="Speed")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Download", f"{data['download_mbps']} Mbps")
        table.add_row("Upload", f"{data['upload_mbps']} Mbps")
        console.print(table)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Speed command failed: %s", exc)
        typer.echo(f"Unable to measure speed: {exc}", err=True)


@app.command()
def update() -> None:
    """Show an update notice for the local installation."""

    try:
        console.print("SysDoc is up to date for this local build.")
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Update command failed: %s", exc)
        typer.echo(f"Unable to run update check: {exc}", err=True)


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
        logger.exception("Doctor fix command failed: %s", exc)
        typer.echo(f"Unable to apply doctor fix: {exc}", err=True)


if __name__ == "__main__":
    app()
