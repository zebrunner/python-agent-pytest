import logging
from typing import Any

from pydantic import ValidationError

from pytest_zebrunner.hooks import PytestZebrunnerHooks
from pytest_zebrunner.settings import ZebrunnerSettings

logger = logging.getLogger(__name__)


def pytest_configure(config: Any) -> None:

    try:
        settings = ZebrunnerSettings()
    except ValidationError as e:
        logger.warning("Missing required config options. Zebrunner plugin hasn't configured", exc_info=e)
        return

    hooks = PytestZebrunnerHooks(settings)
    config.pluginmanager.register(hooks)

    config.addinivalue_line("markers", "maintainer(name): Email or nickname of test maintainer")
    config.addinivalue_line("markers", "skip: Skip test")
