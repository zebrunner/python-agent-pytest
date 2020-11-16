import logging
from pprint import pprint
from typing import Any, Optional

logger = logging.getLogger(__name__)


class DriverInfo:
    __instance = None
    info: Optional[dict] = None

    def __new__(cls, *args, **kwargs) -> Any:  # type: ignore
        if cls.__instance is None:
            cls.__instance = super(DriverInfo, cls).__new__(cls)

        return cls.__instance

    def __init__(self, info: Optional[dict] = None):
        if info is not None:
            self.info = info
        print(info)


def inject_driver() -> None:
    try:
        from selenium import webdriver

        class CustomDriver(webdriver.Chrome):
            def __init__(self, *args, **kwargs) -> None:  # type: ignore
                super().__init__(*args, **kwargs)
                pprint(self.__dict__)
                DriverInfo(self.__dict__)

        webdriver.Chrome = CustomDriver

    except ImportError:
        logger.warning("Selenium library is not installed.")
