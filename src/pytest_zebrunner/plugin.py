import logging
import warnings

from _pytest.config import Config
from pydantic import ValidationError

from pytest_zebrunner.context import zebrunner_context
from pytest_zebrunner.hooks import PytestHooks, XdistHooks
from pytest_zebrunner.settings import load_settings

logger = logging.getLogger(__name__)


def pytest_configure(config: Config) -> None:
    config.addinivalue_line("markers", "maintainer(name): Email or nickname of test maintainer")
    config.addinivalue_line("markers", "label(name, value): Test label")
    config.addinivalue_line("markers", "artifact(path): Attach file to the test")
    config.addinivalue_line("markers", "artifact_reference(name, value): Attach reference to the test")
    config.addinivalue_line("markers", "test_rail_case_id(id): Attach test rail case id")
    config.addinivalue_line("markers", "xray_test_key(id): Attach xray case id")
    config.addinivalue_line("markers", "zephyr_test_case_key(id): Attach zephyr case id")

    try:
        settings = load_settings()
        zebrunner_context.settings = settings
    except ValidationError as exc:
        field_errors = "\n".join([f"\033[93m {e['loc'][0]}\033[0m - {e['msg']}" for e in exc.errors()])
        warnings.warn(
            UserWarning(
                "\033[1;31m Zebrunner plugin not configured properly because missing required config options. "
                "No results will be tracked in zebrunner.\n"
                "Add it to environment variables or .env file.\n" + field_errors + "\n" * 3
            )
        )
        return

    if settings.enabled:
        hooks = PytestHooks()
        config.pluginmanager.register(hooks)
        if config.pluginmanager.get_plugin("xdist") is not None:
            config.pluginmanager.register(XdistHooks())
