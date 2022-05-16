import os
from enum import Enum
from typing import Dict, List, Optional, Type

from pytest_zebrunner.api.models import CiContextModel


class CiType(Enum):
    JENKINS = "JENKINS"
    TEAM_CITY = "TEAM_CITY"
    CIRCLE_CI = "CIRCLE_CI"
    TRAVIS_CI = "TRAVIS_CI"
    BAMBOO = "BAMBOO"


class CiVariables:
    CI_ENV_VARIABLE: str
    CI_TYPE: CiType
    ENV_VARIABLE_PREFIXES: List[str]


class Jenkins(CiVariables):
    """
    Jenkins env variables
    """

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


class TeamCity(CiVariables):
    """
    TeamCity environemt variables
    """

    CI_ENV_VARIABLE = "TEAMCITY_VERSION"
    CI_TYPE = CiType.TEAM_CITY
    ENV_VARIABLE_PREFIXES = [
        "BUILD_",
        "HOSTNAME",
        "SERVER_URL",
        "TEAMCITY_",
    ]


class CircleCi(CiVariables):
    """
    CircleCI environemt variables
    """

    CI_ENV_VARIABLE = "CIRCLECI"
    CI_TYPE = CiType.CIRCLE_CI
    ENV_VARIABLE_PREFIXES = ["CIRCLE", "HOSTNAME"]


class TravisCi(CiVariables):
    """
    CircleCI environemt variables
    """

    CI_ENV_VARIABLE = "TRAVIS"
    CI_TYPE = CiType.TRAVIS_CI
    ENV_VARIABLE_PREFIXES = ["TRAVIS", "USER"]


class CiContextLoader:
    @staticmethod
    def load_context_variables(prefixes: List[str]) -> Dict[str, str]:
        """
        Returns a dictionary with environment variables that start with one of prefixes
        """
        env_variable_names = list(filter(lambda name: any([name.startswith(x) for x in prefixes]), os.environ))
        return {key: os.environ[key] for key in env_variable_names}

    @staticmethod
    def resolve_ci_context() -> Optional[CiContextModel]:
        """
        Go through list of ci variables definitions and try to load variables related to this definition.
        Return first found ci context
        """

        ci_services_variables: List[Type[CiVariables]] = [
            Jenkins,
            TeamCity,
            CircleCi,
            TravisCi,
        ]

        for ci_variables in ci_services_variables:
            if ci_variables.CI_ENV_VARIABLE not in os.environ:
                continue

            return CiContextModel(
                ci_type=ci_variables.CI_TYPE.value,
                env_variables=CiContextLoader.load_context_variables(ci_variables.ENV_VARIABLE_PREFIXES),
            )

        return None
