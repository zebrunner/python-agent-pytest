__all__ = [
    'zafira_state', 'client', 'resource_constants', 'resources', 'plugin', 'listener',
    'connector_obj', 'PyTestZafiraListener', 'handler', 'ZebrunnerRestHandler'
]

import logging
from pprint import pprint

from .plugin import connector_obj
from .listener import PyTestZafiraListener
from .handler import ZebrunnerRestHandler


logger = logging.getLogger('ui')


try:
    from selenium import webdriver

    class CustomDriver(webdriver.Remote):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            pprint(self.__dict__)

    webdriver.WebDriver = CustomDriver
except ImportError:
    logger.warning('Selenium library is not installed.')
