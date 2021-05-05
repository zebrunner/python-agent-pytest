import logging
import warnings
from typing import Union

from _pytest.config import Config
from pydantic import ValidationError

from pytest_zebrunner.hooks import PytestHooks, PytestXdistHooks
from pytest_zebrunner.settings import load_settings

logger = logging.getLogger(__name__)


def pytest_configure(config: Config) -> None:

    try:
        settings = load_settings()
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
        hooks: Union[PytestHooks, PytestXdistHooks]
        print(config.invocation_params.args)
        if config.pluginmanager.has_plugin("xdist") and any([x == "-n" for x in config.invocation_params.args]):
            hooks = PytestXdistHooks()
        else:
            print("SIMPLE HOOKS")
            hooks = PytestHooks()

        config.pluginmanager.register(hooks)
        config.addinivalue_line("markers", "maintainer(name): Email or nickname of test maintainer")
        config.addinivalue_line("markers", "label(name, value): Test label")
