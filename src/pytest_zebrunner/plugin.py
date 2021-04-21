import logging
import warnings
from typing import Any

from pydantic import ValidationError

from pytest_zebrunner.hooks import PytestZebrunnerHooks
from pytest_zebrunner.settings import load_settings

logger = logging.getLogger(__name__)


def pytest_configure(config: Any) -> None:

    try:
        settings = load_settings()
        print(settings)
    except ValidationError as exc:
        field_errors = "\n".join([f"\033[93m {e['loc'][0]}\033[0m - {e['msg']}" for e in exc.errors()])
        warnings.warn(
            UserWarning(
                "\033[1;31m Zebrunner plugin not configured properly because missing required config options.\n"
                "Add it to environment variables or .env file.\n" + field_errors + "\n" * 3
            )
        )
        return

    if settings.enabled:
        hooks = PytestZebrunnerHooks()
        config.pluginmanager.register(hooks)

        config.addinivalue_line("markers", "maintainer(name): Email or nickname of test maintainer")
        config.addinivalue_line("markers", "label(name, value): Test label")
