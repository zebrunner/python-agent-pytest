import logging

import pytest
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo

from pytest_zebrunner.context import TestRun, zebrunner_context
from pytest_zebrunner.reporting_service import ReportingService
from pytest_zebrunner.selenium_integration import SeleniumSession, inject_driver

logger = logging.getLogger(__name__)


class PytestHooks:
    def __init__(self) -> None:
        self.service = ReportingService()
        self.session_manager = SeleniumSession(self.service)
        self.is_worker = True

    @pytest.hookimpl
    def pytest_sessionstart(self, session: Session) -> None:
        self.is_worker = hasattr(session.config, "workerinput")
        if self.is_worker:
            test_run = TestRun(
                zebrunner_context.settings.run.display_name,
                zebrunner_context.settings.run.environment,
                zebrunner_context.settings.run.build,
            )
            test_run.zebrunner_id = session.config.workerinput["test_run_id"]
            zebrunner_context.test_run = test_run
        else:
            self.service.start_test_run()

        inject_driver(self.session_manager)

    @pytest.hookimpl
    def pytest_collection_finish(self, session: Session) -> None:
        session.items = self.service.filter_test_items(session.items)

    @pytest.hookimpl
    def pytest_sessionfinish(self, session: Session, exitstatus: int) -> None:
        if not self.is_worker:
            self.service.finish_test_run()
            self.session_manager.finish_all_sessions()

    @pytest.hookimpl
    def pytest_runtest_makereport(self, item: Item, call: CallInfo) -> TestReport:
        report = TestReport.from_item_and_call(item, call)
        if report.when == "setup":
            self.service.start_test(report, item)
        elif report.when == "call":
            if zebrunner_context.test_is_active:
                self.session_manager.add_test(zebrunner_context.test_id)
            self.service.finish_test(report, item)

        return report


class XdistHooks:
    def pytest_configure_node(self, node):  # type: ignore
        node.workerinput["test_run_id"] = zebrunner_context.test_run.zebrunner_id
