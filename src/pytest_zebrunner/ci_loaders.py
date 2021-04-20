import os
from typing import Dict, List, Optional


class BaseContextLoader:
    @staticmethod
    def load_context_variables(prefixes: List[str]) -> Dict[str, str]:
        env_variable_names = list(filter(lambda name: any([name.startswith(x) for x in prefixes]), os.environ))
        return {key: os.environ[key] for key in env_variable_names}


class JenkinsContextLoader(BaseContextLoader):
    CI_ENV_VARIABLE = "JENKINS_URL"
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
    ENV_VARIABLE_PREFIXES = ["CIRCLE", "HOSTNAME"]

    @classmethod
    def resolve(cls) -> Optional[Dict[str, str]]:
        if cls.CI_ENV_VARIABLE in os.environ:
            return cls.load_context_variables(cls.ENV_VARIABLE_PREFIXES)
        else:
            return None


class TravisCiContextResolver(BaseContextLoader):
    CI_ENV_VARIABLE = "TRAVIS"
    ENV_VARIABLE_PREFIXES = ["TRAVIS", "USER"]

    @classmethod
    def resolve(cls) -> Optional[Dict[str, str]]:
        if cls.CI_ENV_VARIABLE in os.environ:
            return cls.load_context_variables(cls.ENV_VARIABLE_PREFIXES)
        else:
            return None
