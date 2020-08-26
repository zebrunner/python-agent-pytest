import configparser
import logging
from os import getcwd, environ
from enum import Enum

from .exceptions import ConfigError

CONFIG_FILE_PATH = getcwd() + '/zafira_properties.ini'

LOGGER = logging.getLogger('zebrunner')


class Context:

    @staticmethod
    def get(parameter):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)
        LOGGER.debug('Acquiring property {}'.format(parameter.value))
        return config.get('config', parameter.value)


class Parameter(Enum):
    SERVICE_URL = 'service_url'
    ACCESS_TOKEN = 'access_token'
    ZAFIRA_ENABLED = 'zafira_enabled'
    ZAFIRA_PROJECT = 'zafira_project'
    DRIVER_INSTANCE_NAME = 'driver_instance_name'


def get_env_var(env_var_key):
    """
    Getter for environment variable keys.  Uses `os.environ.get(KEYNAME)`
    :param env_key:  Type string.  Key name of environment variable to get.
    :return:  Value of the environment variable.
    """
    env_var_value = environ.get(env_var_key)
    if env_var_value is None:
        LOGGER.error('ENV var missing: [{0}], please set this variable'.format(env_var_key))
        raise ConfigError("Env variable {0} is mandatory, please set this variable".format(env_var_key))
    else:
        LOGGER.debug('ENV variable is: [{0}]:[{1}]'.format(env_var_key, env_var_value))
    return env_var_value
