import os
from typing import Type

import pytest

from pytest_zebrunner import ci_loaders


def test_base_loader() -> None:
    os.environ.update({"IN_LIST": "in_list", "IN_LIST_2": "in_list_2", "OUT_OF_LIST": "out_of_list"})

    variables = ci_loaders.BaseContextLoader.load_context_variables(["IN_LIST"])
    assert variables["IN_LIST"] == "in_list"
    assert variables["IN_LIST_2"] == "in_list_2"
    assert "OUT_OF_LIST" not in variables

    os.environ.pop("IN_LIST")
    os.environ.pop("IN_LIST_2")
    os.environ.pop("OUT_OF_LIST")


@pytest.mark.parametrize(
    "resolver_cls",
    [
        ci_loaders.JenkinsContextLoader,
        ci_loaders.TravisCiContextResolver,
        ci_loaders.CircleCiContextResolver,
        ci_loaders.TeamCityCiContextResolver,
    ],
)
def test_resolvers(resolver_cls: Type) -> None:
    assert resolver_cls.resolve() is None and resolver_cls.CI_ENV_VARIABLE not in os.environ
    os.environ[resolver_cls.CI_ENV_VARIABLE] = "ci"
    assert isinstance(resolver_cls.resolve(), dict)
    os.environ.pop(resolver_cls.CI_ENV_VARIABLE)


@pytest.mark.parametrize(
    "resolver_cls",
    [
        ci_loaders.JenkinsContextLoader,
        ci_loaders.TravisCiContextResolver,
        ci_loaders.CircleCiContextResolver,
        ci_loaders.TeamCityCiContextResolver,
    ],
)
def test_global_resolve(resolver_cls: Type) -> None:
    env_name = resolver_cls.CI_ENV_VARIABLE
    os.environ.update({env_name: "value"})
    ci_context = ci_loaders.resolve_ci_context()
    assert ci_context is not None and ci_context.ci_type == resolver_cls.CI_TYPE.value
    os.environ.pop(env_name)
