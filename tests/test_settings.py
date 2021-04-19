import os
from pathlib import Path
from typing import Any, Generator, List

import pytest
from pydantic.main import BaseModel

from pytest_zebrunner.settings import Settings, ZebrunnerSettings


@pytest.fixture
def yaml_file() -> Generator:
    yaml_file = """
        reporting:
          enabled: true
          server:
            hostname: yaml_hostname
            access-token: yaml_access_token
    """
    path = Path("agent.yaml")
    path.write_text(yaml_file)
    yield
    path.unlink()


@pytest.fixture
def yml_file() -> Generator:
    yml_file = """
        reporting:
          enabled: true
          server:
            hostname: yml_hostname
            access-token: yml_access_token
    """
    path = Path("agent.yml")
    path.write_text(yml_file)
    yield
    path.unlink()


@pytest.fixture
def env_variables() -> Generator:
    os.environ.update(
        {
            "REPORTING_SERVER_HOSTNAME": "env_hostname",
            "REPORTING_SERVER_ACCESS_TOKEN": "env_access_token",
        }
    )
    print("ENVIRONMENT VARIABLES UPDATED")
    yield
    os.environ.pop("REPORTING_SERVER_HOSTNAME")
    os.environ.pop("REPORTING_SERVER_ACCESS_TOKEN")
    print("ENV_VARIUABLES_REMOVED")


def test_simple_model() -> None:
    settings = ZebrunnerSettings()

    class SimpleModel(BaseModel):
        field1 = ""

    assert settings._list_settings(SimpleModel) == [["field1"]]


def test_inner_model() -> None:
    settings = ZebrunnerSettings()

    class SimpleInnerModel(BaseModel):
        inner_field1 = ""

    class SimpleModel(BaseModel):
        inner = SimpleInnerModel()

    assert settings._list_settings(SimpleModel) == [["inner", "inner_field1"]]


def test_combined_model() -> None:
    settings = ZebrunnerSettings()

    class SimpleInnerModel(BaseModel):
        inner_field1 = ""

    class SimpleModel(BaseModel):
        inner = SimpleInnerModel()
        field1 = ""

    assert settings._list_settings(SimpleModel) == [["inner", "inner_field1"], ["field1"]]


@pytest.mark.parametrize(
    "path, value, expected", ((["field1"], 1, {"field1": 1}), (["field1", "field2"], 1, {"field1": {"field2": 1}}))
)
def test_put_by_path(path: List[str], value: Any, expected: dict) -> None:
    data: dict = {}
    ZebrunnerSettings.put_by_path(data, path, value)
    assert data == expected


@pytest.mark.parametrize(
    "data, path, default_value, expected",
    (
        ({}, ["field1"], "default", "default"),
        ({"field1": "value1"}, ["field1"], "default", "value1"),
        ({"field1": {"inner_field1": "inner_value1"}}, ["field1", "inner_field1"], "default", "inner_value1"),
        ({"field1": {"inner_field1": "inner_value1"}}, ["field2", "inner_field1"], "default", "default"),
    ),
)
def test_get_by_path(data: dict, path: List[str], default_value: Any, expected: Any) -> None:
    assert ZebrunnerSettings.get_by_path(data, path, default_value) == expected


def test_combined_put_by_path() -> None:
    data: dict = {}
    ZebrunnerSettings.put_by_path(data, ["field2"], 1)
    ZebrunnerSettings.put_by_path(data, ["field1", "inner_field1"], 1)
    ZebrunnerSettings.put_by_path(data, ["field1", "inner_field2"], 1)
    assert data == {"field2": 1, "field1": {"inner_field1": 1, "inner_field2": 1}}


def test_schema_parsed_without_exceptions() -> None:
    settings = ZebrunnerSettings()
    name_list = settings._list_settings(Settings)
    assert name_list


def test_load_from_env(env_variables) -> None:  # type: ignore
    settings_loader = ZebrunnerSettings()
    settings = settings_loader.load_env(settings_loader._list_settings(Settings))

    assert settings["server"]["hostname"] == "env_hostname"
    assert settings["server"]["access_token"] == "env_access_token"


def test_load_from_yaml(yaml_file: Path) -> None:
    settings_loader = ZebrunnerSettings()
    settings = settings_loader.load_yaml(settings_loader._list_settings(Settings))

    assert settings["server"]["hostname"] == "yaml_hostname"
    assert settings["server"]["access_token"] == "yaml_access_token"
    assert settings["enabled"] is True


def test_load_from_yml(yml_file: Path) -> None:
    settings_loader = ZebrunnerSettings()
    settings = settings_loader.load_yaml(settings_loader._list_settings(Settings))

    assert settings["server"]["hostname"] == "yml_hostname"
    assert settings["server"]["access_token"] == "yml_access_token"
    assert settings["enabled"] is True


def test_load_from_yaml_not_exists() -> None:
    settings_loader = ZebrunnerSettings()
    settings = settings_loader.load_yaml(settings_loader._list_settings(Settings))
    assert settings == {}


def test_load_settings_env_only(env_variables) -> None:  # type: ignore
    settings_loader = ZebrunnerSettings()
    settings = settings_loader.load_settings()

    assert settings.enabled is True
    assert settings.server.hostname == "env_hostname"
    assert settings.server.access_token == "env_access_token"


def test_load_settings_yaml_only(yaml_file) -> None:  # type: ignore
    settings_loader = ZebrunnerSettings()
    settings = settings_loader.load_settings()

    assert settings.server.hostname == "yaml_hostname"
    assert settings.server.access_token == "yaml_access_token"
    assert settings.enabled is True


def test_load_settings_validation_error() -> None:
    settings_loader = ZebrunnerSettings()
    with pytest.raises(ValueError):
        settings_loader.load_settings()


def test_load_settings_overrides(yaml_file, env_variables) -> None:  # type: ignore
    settings_loader = ZebrunnerSettings()
    settings = settings_loader.load_settings()

    assert settings.server.hostname == "env_hostname"
    assert settings.server.access_token == "env_access_token"
