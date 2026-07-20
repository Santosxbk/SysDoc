from sysdoc.utils.installer import build_install_commands, detect_package_manager


def test_build_install_commands_for_linux() -> None:
    commands = build_install_commands("linux")

    assert commands
    assert any("apt-get" in command for command in commands)
    assert any("pip install" in command for command in commands)


def test_detect_package_manager_for_linux() -> None:
    package_manager = detect_package_manager("linux")

    assert package_manager in {"apt", "dnf", "pacman", None}
