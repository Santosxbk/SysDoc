from pathlib import Path

from sysdoc.config import AppConfig, load_config, save_config


def test_load_config_defaults(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config = load_config(config_path)

    assert isinstance(config, AppConfig)
    assert config.language == "pt"
    assert config.theme == "dark"
    assert config.timeout == 5


def test_save_and_load_config(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    expected = AppConfig(colors=True, language="en", theme="light", log_level="DEBUG", timeout=10)

    save_config(expected, config_path)
    loaded = load_config(config_path)

    assert loaded.language == "en"
    assert loaded.theme == "light"
    assert loaded.log_level == "DEBUG"
    assert loaded.timeout == 10
