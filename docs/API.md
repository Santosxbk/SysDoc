# SysDoc API reference

## CLI commands

- scan: runs a quick overview of the system
- cpu: shows CPU metrics and recommendations
- ram: shows RAM metrics and recommendations
- disk: shows disk metrics and recommendations
- gpu: shows GPU information
- battery: shows battery status
- temperatures: shows temperature readings
- network: shows network information
- dns: shows DNS servers
- ping: checks localhost connectivity
- security: shows a basic security assessment
- doctor: runs an intelligent diagnosis
- report: exports TXT, JSON and HTML reports
- version: shows version information
- init: writes a default configuration file

## Extension points

The core modules are organized under:

- sysdoc.diagnostics for analysis helpers
- sysdoc.hardware for hardware collectors
- sysdoc.network for connectivity helpers
- sysdoc.reports for exporters
- sysdoc.security for security checks
- sysdoc.utils for system utilities
