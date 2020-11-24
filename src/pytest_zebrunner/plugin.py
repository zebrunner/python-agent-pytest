import logging
from logging import error
from typing import Any
import warnings

from pydantic import ValidationError

from pytest_zebrunner.hooks import PytestZebrunnerHooks
from pytest_zebrunner.settings import ZebrunnerSettings

logger = logging.getLogger(__name__)


def pytest_configure(config: Any) -> None:

    try:
        settings = ZebrunnerSettings()
    except ValidationError as exc:
        field_errors = "\n".join([f"{e['loc'][0]} - {e['msg']}" for e in exc.errors()])
        warnings.warn(
            UserWarning(
                "Zebrunner plugin not configured properly because missing required config options.\n"
                "Add it to environment variables or .env file.\n" + field_errors
            )
        )
        return

    hooks = PytestZebrunnerHooks(settings)
    config.pluginmanager.register(hooks)

    config.addinivalue_line("markers", "maintainer(name): Email or nickname of test maintainer")
    config.addinivalue_line("markers", "skip: Skip test")
