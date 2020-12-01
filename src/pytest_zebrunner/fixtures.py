from logging import warning
from typing import Callable

import pytest

from pytest_zebrunner.context import zebrunner_context
from pytest_zebrunner.zebrunner_api.client import ZebrunnerAPI


@pytest.fixture(scope="session")
def send_screenshot() -> Callable:
    def _send_screenshot(image_path: str) -> None:
        api = ZebrunnerAPI()
        if zebrunner_context.test_id and zebrunner_context.test_run_id and api.authenticated:
            api.send_screenshot(zebrunner_context.test_run_id, zebrunner_context.test_id, image_path)
        else:
            warning(
                UserWarning("There's problems with running test session. Cant't push screenshot."),
                extra={
                    "test_id": zebrunner_context.test_id,
                    "test_run_id": zebrunner_context.test_run_id,
                    "authenticated": api.authenticated,
                },
            )

    return _send_screenshot


@pytest.fixture(scope="session")
def send_artifact() -> Callable:
    def _send_artifact(filename: str) -> None:
        api = ZebrunnerAPI()
        if zebrunner_context.test_run_id and zebrunner_context.test_id:
            api.send_artifact(zebrunner_context.test_run_id, zebrunner_context.test_id, filename)

    return _send_artifact
