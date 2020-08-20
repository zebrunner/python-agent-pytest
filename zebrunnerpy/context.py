import configparser
import logging
from os import getcwd, environ
from enum import Enum

from .exceptions import ConfigError

logger = logging.getLogger('settings')

CONFIG_FILE_PATH = getcwd() + '/zafira_properties.ini'


class Context:

    @staticmethod
    def get(parameter):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)
        return config.get('config', parameter.value)


class Parameter(Enum):
    SERVICE_URL = 'service-url'
    ACCESS_TOKEN = 'access_token'
    ZAFIRA_ENABLED = 'zafira_enabled'
    JOB_NAME = 'job_name'
    ARTIFACT_EXPIRES_IN_DEFAULT_TIME = 'artifact_expires_in_default_time'
    ARTIFACT_LOG_NAME = 'artifact_log_name'
    AWS_SCREEN_SHOT_BUCKET = 'aws_screen_shot_bucket'
    S3_SAVE_SCREENSHOTS = 's3_save_screenshots'


def get_env_var(env_var_key):
    """
    Getter for environment variable keys.  Uses `os.environ.get(KEYNAME)`
    :param env_key:  Type string.  Key name of environment variable to get.
    :return:  Value of the environment variable.
    """
    env_var_value = environ.get(env_var_key)
    if env_var_value is None:
        logger.error('ENV var missing: [{0}], please set this variable'.format(env_var_key))
        raise ConfigError("Env variable {0} is mandatory, please set this variable".format(env_var_key))
    else:
        logger.debug('ENV variable is: [{0}]:[{1}]'.format(env_var_key, env_var_value))
    return env_var_value
