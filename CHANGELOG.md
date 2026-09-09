# Changelog

## [1.0.0] - 2026-09-09

### Added
- Formal first stable release of SysDoc
- Rich CLI with structured output and JSON flag support for automation
- Comprehensive diagnostics across CPU, RAM, disk, network, DNS, GPU, battery and temperature
- Security posture checks and doctor recommendations
- Report export to TXT, JSON and HTML
- Installation guidance and platform-aware setup commands

### Improved
- Hardened handling for missing hardware and sensor data in containerized environments
- More robust network gateway detection across different Linux interface names
- Safer output rendering for unknown or unavailable values
- Better CLI error handling and consistent version reporting
- Package metadata and import reliability for CI and local installs

### Fixed
- Fixes for absent GPU, battery and temperature readings
- Fixes for gateway detection issues on non-standard interfaces
- Fixes for package import/export and HTML report generation in minimal environments
- Compatibility improvements for Typer and installation workflow stability

## [0.1.0] - 2026-07-20

### Added
- Initial project structure for SysDoc
- Typer-based CLI with scan, cpu, ram, disk, version and init commands
- Rich banner and table-based UI
- YAML configuration support
- Logging configuration with file and console handlers
- Core system information helpers for OS, CPU, RAM and disk
- Pytest-based unit tests for configuration and system helpers
- Network interface and gateway diagnostics
- DNS server lookup and hostname resolution
- Ping checks and public IP lookup
- CPU usage analysis and recommendations
- RAM pressure analysis and recommendations
- Disk utilization analysis and recommendations
- GPU detection and reporting
- Battery status and remaining runtime
- Temperature sensor reporting when available
- Basic security posture assessment
- Intelligent system diagnosis across CPU, memory and disk
- TXT, JSON and HTML report export
- Automated installation guidance for Python dependencies and external tools
