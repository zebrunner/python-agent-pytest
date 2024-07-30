import logging
from typing import Optional

from pytest_zebrunner.api.models import LabelModel, PlatformModel

from .api.client import ZebrunnerAPI
from .context import zebrunner_context
from .errors import AgentApiError, AgentError


class CurrentTestRun:
    @staticmethod
    def set_build(build: str) -> None:
        if not build.strip():
            raise AgentError("Build must not be empty")

        if not zebrunner_context.test_run_is_active:
            raise AgentError("There is not active test run to set build")

        settings = zebrunner_context.settings
        try:
            api = ZebrunnerAPI(settings.server.hostname, settings.server.access_token)
            api.patch_test_run_build(zebrunner_context.test_run_id, build)
        except AgentApiError as e:
            logging.error("Failed to set build", exc_info=e)

    @staticmethod
    def set_locale(locale: str) -> None:
        if not locale.strip():
            raise AgentError("Locale must no be empty")
        if not zebrunner_context.test_run_is_active:
            raise AgentError("There is not active test run to set locale")

        label = "com.zebrunner.app/sut.locale"
        settings = zebrunner_context.settings
        try:
            api = ZebrunnerAPI(settings.server.hostname, settings.server.access_token)
            api.send_labels([LabelModel(key=label, value=locale)], zebrunner_context.test_run_id, None)
        except AgentApiError as e:
            logging.error("failed to set locale", exc_info=e)

    @staticmethod
    def set_platform(name: str) -> None:
        if not name.strip():
            raise AgentError("Platform must not be empty")

        CurrentTestRun.set_platform_version(name, None)

    @staticmethod
    def set_platform_version(name: str, version: Optional[str]) -> None:
        if not name.strip():
            raise AgentError("Platform must not be empty")
        if not zebrunner_context.test_run_is_active:
            raise AgentError("There is not active test run to set platform")

        settings = zebrunner_context.settings
        try:
            api = ZebrunnerAPI(settings.server.hostname, settings.server.access_token)
            api.set_test_run_platform(
                zebrunner_context.test_run_id,
                PlatformModel(name=name, version=version),
            )
        except AgentApiError as e:
            logging.error("Failed to set platform", exc_info=e)
