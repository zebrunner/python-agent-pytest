import copy
import logging
from typing import Any, Dict

from pytest_zebrunner.context import zebrunner_context

logger = logging.getLogger(__name__)


class SeleniumSession:
    def __init__(self, reporting_service) -> None:  # type: ignore
        self._active_sessions: Dict[str, Any] = {}
        self.reporting_service = reporting_service

    def start_session(self, session_id: str, capabilities: dict, desired_capabilities: dict) -> None:
        self._active_sessions[session_id] = {"related_tests": []}
        if zebrunner_context.test_is_active:
            self._active_sessions[session_id]["related_tests"].append(zebrunner_context.test_id)

        zebrunner_session_id = self.reporting_service.start_test_session(
            session_id, capabilities, desired_capabilities, self._active_sessions[session_id]["related_tests"]
        )
        if zebrunner_session_id:
            self._active_sessions[session_id]["zebrunner_session_id"] = zebrunner_session_id

    def finish_session(self, session_id: str) -> None:
        self.reporting_service.finish_test_session(
            self._active_sessions[session_id]["zebrunner_session_id"],
            self._active_sessions[session_id]["related_tests"],
        )
        del self._active_sessions[session_id]

    def finish_all_sessions(self) -> None:
        for session_id in list(self._active_sessions):
            self.finish_session(session_id)

    def add_test(self, test_id: int) -> None:
        for session_id in self._active_sessions:
            if self._active_sessions[session_id].get("related_tests") is not None:
                self._active_sessions[session_id]["related_tests"].append(test_id)
            else:
                self._active_sessions[session_id]["related_tests"] = [test_id]


def inject_driver(session_manager: SeleniumSession) -> None:
    try:
        from selenium.webdriver.remote.webdriver import WebDriver

        base_init = WebDriver.__init__
        base_quit = WebDriver.quit

        def init(  # type: ignore
            session: WebDriver,
            command_executor: str = "http://127.0.0.1:4444/wd/hub",
            desired_capabilities: dict = None,
            browser_profile=None,
            proxy=None,
            keep_alive: bool = False,
            file_detector=None,
            options=None,
        ) -> None:  # type: ignore
            # Override capabilities and command_executor with new ones provided by zebrunner.
            caps = copy.deepcopy(desired_capabilities)
            if zebrunner_context.settings.zebrunner:
                zeb_settings = zebrunner_context.settings.zebrunner
                if zeb_settings.hub_url:
                    command_executor = zeb_settings.hub_url
                if zeb_settings.desired_capabilities and caps:
                    caps.update(zeb_settings.desired_capabilities)

            base_init(
                session,
                command_executor,
                caps,
                browser_profile,
                proxy,
                keep_alive,
                file_detector,
                options,
            )
            session_manager.start_session(session.session_id, session.capabilities, desired_capabilities or {})
            if zebrunner_context.test_is_active:
                session_manager.add_test(zebrunner_context.test_id)

        def quit(session) -> None:  # type: ignore
            session_manager.finish_session(session.session_id)
            base_quit(session)

        WebDriver.__init__ = init
        WebDriver.quit = quit

    except ImportError:
        logger.warning("Selenium library is not installed.")
