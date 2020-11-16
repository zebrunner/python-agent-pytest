import logging

from .selenium_driver import inject_driver

logging.basicConfig(level=logging.DEBUG)
inject_driver()

__version__ = "0.1.0"
