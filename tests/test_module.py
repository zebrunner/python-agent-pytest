from pathlib import Path

from pytest_zebrunner import __version__ as package_version


def test_version_is_match() -> None:
    pyproject_text = Path("pyproject.toml").read_text()
    version_line = list(filter(lambda line: line.startswith("version ="), pyproject_text.split("\n")))[0]
    version = version_line.split(" ")[-1].replace('"', "")
    assert version == package_version
