import logging
from pprint import pprint

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("ui")


try:
    from selenium import webdriver

    class CustomDriver(webdriver.Remote):
        def __init__(self, *args, **kwargs) -> None:  # type: ignore
            super().__init__(*args, **kwargs)
            pprint(self.__dict__)

    webdriver.WebDriver = CustomDriver
except ImportError:
    logger.warning("Selenium library is not installed.")

__version__ = "0.1.0"
