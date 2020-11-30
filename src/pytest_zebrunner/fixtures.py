from typing import Callable

import pytest

from pytest_zebrunner.context import zebrunner_context


@pytest.fixture(scope="session")
def send_screenshot() -> Callable:
    def _send_screenshot() -> None:
        print(f"screenshot for {zebrunner_context.test_run_id}, {zebrunner_context.test_id} was sent")

    return _send_screenshot
