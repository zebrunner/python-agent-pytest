import itertools
import logging
from typing import Generator

import pytest
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo

from pytest_zebrunner.context import TestRun, zebrunner_context
from pytest_zebrunner.reporting_service import ReportingService
from pytest_zebrunner.selenium_integration import SeleniumSessionManager, inject_driver

logger = logging.getLogger(__name__)


class PytestHooks:
    def __init__(self) -> None:
        self.service = ReportingService()
        self.session_manager = SeleniumSessionManager(self.service)
        self.is_worker = True
        self.is_controller = False

    @pytest.hookimpl
    def pytest_sessionstart(self, session: Session) -> None:
        self.is_worker = hasattr(session.config, "workerinput")
        self.is_controller = getattr(session.config.option, "dist", "no") != "no"
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
            self.session_manager.finish_all_sessions()
            self.service.finish_test_run()
            self.service.api.close()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item: Item, call: CallInfo) -> Generator:
        outcome = yield
        report: TestReport = outcome.get_result()

        report.maintainers = [str(mark.args[0]) for mark in item.iter_markers("maintainer")]
        report.labels = [(str(mark.args[0]), str(mark.args[1])) for mark in item.iter_markers("label")]
        report.artifact_references = [
            (str(m.args[0]), str(m.args[1])) for m in item.iter_markers("artifact_reference")
        ]
        report.artifacts = [mark.args[0] for mark in item.iter_markers("artifact")]
        report.test_rail_case_ids = list(
            itertools.chain(*[mark.args for mark in item.iter_markers("test_rail_case_id")])
        )
        report.xray_case_ids = list(itertools.chain(*[mark.args for mark in item.iter_markers("xray_test_key")]))
        report.zephyr_case_ids = list(
            itertools.chain(*[mark.args for mark in item.iter_markers("zephyr_test_case_key")])
        )

    @pytest.hookimpl
    def pytest_runtest_logreport(self, report: TestReport) -> None:
        if self.is_worker or not self.is_controller:
            is_setup_rerun = hasattr(report, "rerun") and report.rerun > 0
            is_call_rerun = report.outcome == "rerun"
            if report.when == "setup" and not is_setup_rerun:
                self.service.start_test(report)
                if zebrunner_context.test_is_active:
                    self.session_manager.add_test(zebrunner_context.test_id)

                if report.outcome == "skipped":
                    self.service.finish_test(report)
            elif report.when == "call" and not is_call_rerun:
                self.service.finish_test(report)


class XdistHooks:
    def pytest_configure_node(self, node):  # type: ignore
        node.workerinput["test_run_id"] = zebrunner_context.test_run.zebrunner_id
