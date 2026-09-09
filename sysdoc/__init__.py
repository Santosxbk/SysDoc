"""SysDoc package."""

from importlib.metadata import PackageNotFoundError, version

from .config import AppConfig, load_config, save_config


def _get_version() -> str:
    """Return the installed package version, or a fallback string."""

    try:
        return version("sysdoc")
    except PackageNotFoundError:
        return "1.0.0"


__version__ = _get_version()

__all__ = ["AppConfig", "load_config", "save_config", "__version__"]
