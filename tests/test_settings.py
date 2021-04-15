from typing import Any, List

import pytest
from pydantic.main import BaseModel

from pytest_zebrunner.settings import Settings, ZebrunnerSettings

# @pytest.mark.parametrize("input, expected", [
#     ({"name": "value"}, [["name"]]),
#     ({"name": {"inner_name": "inner_value"}}, [["name" , "inner_name"]]),
#     ({"name": {"inner_name": "inner_value"}, "name2": "value2"}, [["name", "inner_name"], ["name2"]]),
#     ({}, [])
# ])
# def test_list_settings(input: dict, expected: list) -> None:
#     settings = ZebrunnerSettings()
#     name_list = settings._list_settings(input)
#     assert name_list == expected


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
