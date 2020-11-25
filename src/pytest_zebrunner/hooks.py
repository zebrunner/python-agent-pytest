import logging
from asyncio import get_event_loop
from typing import Optional, Union

import pytest
from _pytest.config import Config, ExitCode
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo

from pytest_zebrunner.selenium_integration import SeleniumSession, inject_driver
from pytest_zebrunner.settings import ZebrunnerSettings
from pytest_zebrunner.zebrunner_api.client import ZebrunnerAPI
from pytest_zebrunner.zebrunner_api.models import (
    FinishTestModel,
    StartTestModel,
    StartTestRunModel,
    TestRunConfigModel,
    TestStatus,
)

logger = logging.getLogger(__name__)


class PytestZebrunnerHooks:
    def __init__(self, settings: ZebrunnerSettings):
        self.event_loop = get_event_loop()
        self.settings = settings

        self.api = ZebrunnerAPI(self.settings.service_url, self.settings.access_token)

        self.event_loop.run_until_complete(self.api.auth())
        self.session_manager = SeleniumSession(self.api)
        inject_driver(self.session_manager)

        self.test_run_id: Optional[int] = None
        self.test_id: Optional[int] = None

    @pytest.hookimpl
    def pytest_sessionstart(self, session: Session) -> None:
        self.test_run_id = self.event_loop.run_until_complete(
            self.api.start_test_run(
                self.settings.zebrunner_project,
                StartTestRunModel(
                    name=self.settings.suite or "Unnamed",
                    framework="pytest",
                    config=TestRunConfigModel(
                        environment=self.settings.env, suite=self.settings.suite, build=self.settings.build
                    ),
                ),
            )
        )

    @pytest.hookimpl
    def pytest_sessionfinish(self, session: Session, exitstatus: Union[int, ExitCode]) -> None:
        if not self.test_run_id:
            return

        self.event_loop.run_until_complete(self.api.finish_test_run(self.test_run_id))
        self.event_loop.run_until_complete(self.session_manager.finish_all_sessions())
        self.event_loop.run_until_complete(self.api.close())

    @pytest.hookimpl
    def pytest_runtest_makereport(self, item: Item, call: CallInfo) -> TestReport:
        report = TestReport.from_item_and_call(item, call)
        report.item = item  # type: ignore
        return report

    @pytest.hookimpl
    def pytest_report_teststatus(self, report: TestReport, config: Config) -> None:
        if report.when == "setup":
            self.setup_test(report)
        elif report.when == "call":
            self.call_test(report)

    def setup_test(self, report: TestReport) -> None:
        if not self.test_run_id:
            return

        test_item: Item = report.item

        test_name = test_item.name
        class_name = test_item.nodeid.split("::")[1]
        maintainer = ",".join([mark.args[0] for mark in test_item.iter_markers("maintainer")])

        self.test_id = self.event_loop.run_until_complete(
            self.api.start_test(
                self.test_run_id,
                StartTestModel(
                    name=test_name,
                    class_name=class_name,
                    method_name=test_name,
                    maintainer=maintainer or None,
                ),
            )
        )

        if report.skipped and self.test_id:
            skip_markers = list(filter(lambda x: x.name == "skip", report.item.own_markers))
            skip_reson = skip_markers[0].kwargs.get("reason") if skip_markers else None
            self.event_loop.run_until_complete(
                self.api.finish_test(
                    self.test_run_id, self.test_id, FinishTestModel(reason=skip_reson, result=TestStatus.SKIPPED.value)
                )
            )
            self.test_id = None
            return

        self.session_manager.add_test(str(self.test_id))

    def call_test(self, report: TestReport) -> None:
        if not self.test_id or not self.test_run_id:
            return

        if report.skipped:
            self.event_loop.run_until_complete(
                self.api.finish_test(
                    self.test_run_id,
                    self.test_id,
                    FinishTestModel(result=TestStatus.SKIPPED.value, reason=report.wasxfail or None),
                )
            )
            self.test_id = None
            return

        if report.passed:
            status = TestStatus.PASSED
        else:
            status = TestStatus.FAILED

        finish_test_data = FinishTestModel(result=status.value)
        self.event_loop.run_until_complete(self.api.finish_test(self.test_run_id, self.test_id, finish_test_data))
