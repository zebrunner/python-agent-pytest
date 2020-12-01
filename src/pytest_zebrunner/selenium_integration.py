import logging
from typing import Any, Dict

from pytest_zebrunner.zebrunner_api.client import ZebrunnerAPI
from pytest_zebrunner.zebrunner_api.models import (
    FinishTestSessionModel,
    StartTestSessionModel,
)

logger = logging.getLogger(__name__)


class SeleniumSession:
    def __init__(self, api: ZebrunnerAPI) -> None:
        self._active_sessions: Dict[str, Any] = {}
        self.api = api

    def start_session(self, session_id: str, capabilities: dict, desired_capabilities: dict) -> None:
        self._active_sessions[session_id] = {"related_tests": []}

        zebrunner_session_id = self.api.start_test_session(
            StartTestSessionModel(
                session_id=session_id, desired_capabilities=desired_capabilities, capabilities=capabilities
            )
        )
        self._active_sessions[session_id]["zebrunner_session_id"] = zebrunner_session_id

    def finish_session(self, session_id: str) -> None:
        self.api.finish_test_session(
            self._active_sessions[session_id]["zebrunner_session_id"],
            FinishTestSessionModel(test_refs=self._active_sessions[session_id]["related_tests"]),
        )
        del self._active_sessions[session_id]

    def finish_all_sessions(self) -> None:
        for session_id in list(self._active_sessions):
            self.finish_session(session_id)

    def add_test(self, test_id: str) -> None:
        for sesion_id in self._active_sessions:
            if self._active_sessions[sesion_id].get("related_tests") is not None:
                self._active_sessions[sesion_id]["related_tests"].append(test_id)
            else:
                self._active_sessions[sesion_id]["related_tests"] = [test_id]


def inject_driver(session_manager: SeleniumSession) -> None:
    try:
        from selenium.webdriver.remote.webdriver import WebDriver

        base_init = WebDriver.__init__

        def init(session, *args, **kwargs) -> None:  # type: ignore
            base_init(session, *args, **kwargs)
            session_manager.start_session(session.session_id, session.capabilities, session.desired_capabilities)

        WebDriver.__init__ = init

    except ImportError:
        logger.warning("Selenium library is not installed.")
