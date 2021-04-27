import os
from enum import Enum
from typing import Dict, List, Optional, Type

from pytest_zebrunner.api.models import CiContextModel


class BaseContextLoader:
    @staticmethod
    def load_context_variables(prefixes: List[str]) -> Dict[str, str]:
        env_variable_names = list(filter(lambda name: any([name.startswith(x) for x in prefixes]), os.environ))
        return {key: os.environ[key] for key in env_variable_names}


class CiType(Enum):
    JENKINS = "JENKINS"
    TEAM_CITY = "TEAM_CITY"
    CIRCLE_CI = "CIRCLE_CI"
    TRAVIS_CI = "TRAVIS_CI"
    BAMBOO = "BAMBOO"


class JenkinsContextLoader(BaseContextLoader):
    CI_ENV_VARIABLE = "JENKINS_URL"
    CI_TYPE = CiType.JENKINS
    ENV_VARIABLE_PREFIXES = [
        "CVS_",
        "SVN_",
        "GIT_",
        "NODE_",
        "EXECUTOR_NUMBER",
        "JENKINS_",
        "JOB_",
        "BUILD_",
        "ROOT_BUILD_",
        "RUN_",
        "WORKSPACE",
    ]

    @classmethod
    def resolve(cls) -> Optional[Dict[str, str]]:
        if cls.CI_ENV_VARIABLE in os.environ:
            return cls.load_context_variables(cls.ENV_VARIABLE_PREFIXES)
        else:
            return None


class TeamCityCiContextResolver(BaseContextLoader):
    CI_ENV_VARIABLE = "TEAMCITY_VERSION"
    CI_TYPE = CiType.TEAM_CITY
    ENV_VARIABLE_PREFIXES = [
        "BUILD_",
        "HOSTNAME",
        "SERVER_URL",
        "TEAMCITY_",
    ]

    @classmethod
    def resolve(cls) -> Optional[Dict[str, str]]:
        if cls.CI_ENV_VARIABLE in os.environ:
            return cls.load_context_variables(cls.ENV_VARIABLE_PREFIXES)
        else:
            return None


class CircleCiContextResolver(BaseContextLoader):
    CI_ENV_VARIABLE = "CIRCLECI"
    CI_TYPE = CiType.CIRCLE_CI
    ENV_VARIABLE_PREFIXES = ["CIRCLE", "HOSTNAME"]

    @classmethod
    def resolve(cls) -> Optional[Dict[str, str]]:
        if cls.CI_ENV_VARIABLE in os.environ:
            return cls.load_context_variables(cls.ENV_VARIABLE_PREFIXES)
        else:
            return None


class TravisCiContextResolver(BaseContextLoader):
    CI_ENV_VARIABLE = "TRAVIS"
    CI_TYPE = CiType.TRAVIS_CI
    ENV_VARIABLE_PREFIXES = ["TRAVIS", "USER"]

    @classmethod
    def resolve(cls) -> Optional[Dict[str, str]]:
        if cls.CI_ENV_VARIABLE in os.environ:
            return cls.load_context_variables(cls.ENV_VARIABLE_PREFIXES)
        else:
            return None


def resolve_ci_context() -> Optional[CiContextModel]:
    ci_tools: List[Type[BaseContextLoader]] = [
        JenkinsContextLoader,
        TeamCityCiContextResolver,
        CircleCiContextResolver,
        TravisCiContextResolver,
    ]

    ci_context: Optional[Type] = None
    for resolver in ci_tools:
        env_variables = resolver.resolve()  # type: ignore
        if env_variables:
            ci_context = resolver
            break

    if ci_context:
        return CiContextModel(ci_type=ci_context.CI_TYPE.value, env_variables=ci_context.resolve())
    else:
        return None
