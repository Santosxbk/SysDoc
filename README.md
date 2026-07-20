# SysDoc

Modern cross-platform system diagnostics toolkit for Linux, Windows and macOS.

SysDoc provides a polished terminal experience to inspect hardware health, network connectivity, system performance, security posture and generated reports from a single command-line interface.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue" alt="Python 3.12+" />
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License" />
  <img src="https://img.shields.io/badge/Tests-pytest-brightgreen" alt="Pytest" />
</p>

---

## Features

- Rich CLI with Typer and Rich
- CPU, RAM and disk diagnostics
- Network and DNS inspection
- GPU, battery and temperature checks
- Security posture summary
- Intelligent system doctor recommendations
- TXT, JSON and HTML report export
- Optional real speedtest and nmap integrations when tools are installed
- Logging and configuration support

---

## Installation

### From source

```bash
git clone https://github.com/Santosxbk/SysDoc.git
cd SysDoc
python -m pip install -r requirements.txt
```

### From PyPI

```bash
pip install sysdoc
```

---

## Quick start

```bash
python main.py scan
python main.py cpu
python main.py ram
python main.py disk
python main.py network
python main.py dns
python main.py ping
python main.py doctor
python main.py report
```

After installation, you can also run:

```bash
sysdoc scan
```

---

## Available commands

- scan
- cpu
- ram
- disk
- gpu
- battery
- temperatures
- network
- dns
- ping
- ports
- nmap
- speed
- security
- doctor
- doctor-fix
- report
- version
- init

---

## Project structure

```text
sysdoc/
  cli/
  diagnostics/
  hardware/
  network/
  reports/
  security/
  ui/
  utils/
  __init__.py
  config.py
  logging_config.py

tests/
main.py
pyproject.toml
requirements.txt
```

---

## Development

Run the test suite:

```bash
pytest -q
```

Build the package:

```bash
python -m build
```

---

## Verification

The current implementation has been verified with:

```bash
pytest -q
```

Result: 11 passed.

---

## License

This project is licensed under the MIT License.
