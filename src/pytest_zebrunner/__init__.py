__all__ = [
    'zafira_state', 'client', 'resource_constants', 'resources', 'plugin', 'listener',
    'connector_obj', 'PyTestZafiraListener', 'handler', 'ZebrunnerRestHandler'
]

__version__ = '0.1.0'

import logging
from pprint import pprint
from typing import Any

from .handler import ZebrunnerRestHandler
from .listener import PyTestZafiraListener
from .plugin import connector_obj

logger = logging.getLogger('ui')


try:
    from selenium import webdriver

    class CustomDriver(webdriver.Remote):
        def __init__(self, *args: Any, **kwargs: Any):
            super().__init__(*args, **kwargs)
            pprint(self.__dict__)

    webdriver.WebDriver = CustomDriver
except ImportError:
    logger.warning('Selenium library is not installed.')
