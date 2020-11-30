from asyncio import get_event_loop
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
            event_loop = get_event_loop()
            event_loop.run_until_complete(
                api.send_screenshot(zebrunner_context.test_run_id, zebrunner_context.test_id, image_path)
            )
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
