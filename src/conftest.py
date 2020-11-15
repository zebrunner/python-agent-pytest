from typing import Any

from pytest_zebrunner.hooks import PytestZebrunnerHooks
from pytest_zebrunner.settings import ZebrunnerSettings


def pytest_configure(config: Any) -> None:
    settings = ZebrunnerSettings()
    hooks = PytestZebrunnerHooks(settings)

    config.pluginmanager.register(hooks)

    config.addinivalue_line("markers", "maintainer(name): Email or nickname of test maintainer")
    config.addinivalue_line("markers", "skip: Skip test")
