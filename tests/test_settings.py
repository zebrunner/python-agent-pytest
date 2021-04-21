import os
from pathlib import Path
from typing import Any, Generator, List

import pytest
import yaml
from pydantic.main import BaseModel

from pytest_zebrunner import settings


@pytest.fixture
def yaml_file(tmpdir: str) -> Generator:
    yaml_data = {
        "reporting": {"enabled": True, "server": {"hostname": "yaml_hostname", "access-token": "yaml_access_token"}}
    }
    current_directory = os.getcwd()
    os.chdir(tmpdir)
    path = Path("agent.yaml")
    with open(path, "w") as yaml_file:
        yaml.dump(yaml_data, yaml_file)
    yield
    path.unlink()
    os.chdir(current_directory)


@pytest.fixture
def yml_file(tmpdir: str) -> Generator:
    yml_data = {
        "reporting": {"enabled": True, "server": {"hostname": "yml_hostname", "access-token": "yml_access_token"}}
    }
    current_directory = os.getcwd()
    os.chdir(tmpdir)
    path = Path("agent.yaml")
    with open(path, "w") as yml_file:
        yaml.dump(yml_data, yml_file)
    yield
    path.unlink()
    os.chdir(current_directory)


@pytest.fixture
def env_variables() -> Generator:
    os.environ.update(
        {
            "REPORTING_SERVER_HOSTNAME": "env_hostname",
            "REPORTING_SERVER_ACCESS_TOKEN": "env_access_token",
        }
    )
    yield
    os.environ.pop("REPORTING_SERVER_HOSTNAME")
    os.environ.pop("REPORTING_SERVER_ACCESS_TOKEN")


@pytest.fixture
def env_file(tmpdir: str) -> Generator:
    env_file = """
        REPORTING_SERVER_HOSTNAME=env_file_hostname
        REPORTING_SERVER_ACCESS_TOKEN=env_file_access_token
    """
    current_directory = os.getcwd()
    os.chdir(tmpdir)
    path = Path(".env")
    path.write_text(env_file)
    yield
    path.unlink()
    os.chdir(current_directory)


def test_simple_model() -> None:
    class SimpleModel(BaseModel):
        field1 = ""

    assert settings._list_settings(SimpleModel) == [["field1"]]


def test_inner_model() -> None:
    class SimpleInnerModel(BaseModel):
        inner_field1 = ""

    class SimpleModel(BaseModel):
        inner = SimpleInnerModel()

    assert settings._list_settings(SimpleModel) == [["inner", "inner_field1"]]


def test_combined_model() -> None:
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
    settings._put_by_path(data, path, value)
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
    assert settings._get_by_path(data, path, default_value) == expected


def test_combined_put_by_path() -> None:
    data: dict = {}
    settings._put_by_path(data, ["field2"], 1)
    settings._put_by_path(data, ["field1", "inner_field1"], 1)
    settings._put_by_path(data, ["field1", "inner_field2"], 1)
    assert data == {"field2": 1, "field1": {"inner_field1": 1, "inner_field2": 1}}


def test_schema_parsed_without_exceptions() -> None:
    name_list = settings._list_settings(settings.Settings)
    assert name_list


def test_load_from_env(env_variables) -> None:  # type: ignore
    data = settings._load_env(settings._list_settings(settings.Settings))

    assert data["server"]["hostname"] == "env_hostname"
    assert data["server"]["access_token"] == "env_access_token"


def test_load_from_yaml(yaml_file) -> None:  # type: ignore
    data = settings._load_yaml(settings._list_settings(settings.Settings))

    assert data["server"]["hostname"] == "yaml_hostname"
    assert data["server"]["access_token"] == "yaml_access_token"
    assert data["enabled"] is True


def test_load_from_yml(yml_file) -> None:  # type: ignore
    data = settings._load_yaml(settings._list_settings(settings.Settings))

    assert data["server"]["hostname"] == "yml_hostname"
    assert data["server"]["access_token"] == "yml_access_token"
    assert data["enabled"] is True


def test_load_from_yaml_not_exists(tmpdir: str) -> None:
    currend_directory = os.getcwd()
    os.chdir(tmpdir)
    data = settings._load_yaml(settings._list_settings(settings.Settings))
    assert data == {}
    os.chdir(currend_directory)


def test_load_settings_env_only(env_variables) -> None:  # type: ignore
    data = settings.load_settings()

    assert data.enabled is True
    assert data.server.hostname == "env_hostname"
    assert data.server.access_token == "env_access_token"


def test_load_settings_yaml_only(yaml_file) -> None:  # type: ignore
    data = settings.load_settings()

    assert data.server.hostname == "yaml_hostname"
    assert data.server.access_token == "yaml_access_token"
    assert data.enabled is True


def test_load_settings_validation_error() -> None:
    with pytest.raises(ValueError):
        settings.load_settings()


def test_load_settings_overrides(yaml_file, env_variables) -> None:  # type: ignore
    data = settings.load_settings()

    assert data.server.hostname == "env_hostname"
    assert data.server.access_token == "env_access_token"


def test_load_settings_env_file(env_file) -> None:  # type: ignore
    data = settings.load_settings()

    assert data.server.hostname == "env_file_hostname"
    assert data.server.access_token == "env_file_access_token"
