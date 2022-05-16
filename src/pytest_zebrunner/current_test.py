import logging

from pytest_zebrunner.api.client import ZebrunnerAPI
from pytest_zebrunner.context import zebrunner_context
from pytest_zebrunner.errors import AgentApiError, AgentError


class CurrentTest:
    @staticmethod
    def revert_registration() -> None:
        if not zebrunner_context.test_is_active:
            raise AgentError("There is not active test to revert")

        settings = zebrunner_context.settings
        try:
            api = ZebrunnerAPI(settings.server.hostname, settings.server.access_token)
            api.reverse_test_registration(zebrunner_context.test_run_id, zebrunner_context.test_id)
            if zebrunner_context.test:
                zebrunner_context.test.is_reverted = True
        except AgentApiError as e:
            logging.error("Failed to revert test registration", exc_info=e)
