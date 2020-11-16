import logging
from asyncio import get_event_loop
from typing import Optional, Union

import pytest
from _pytest.config import ExitCode
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo

from pytest_zebrunner.selenium_driver import DriverInfo
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

        self.test_run_id: Optional[int] = None
        self.test_id: Optional[int] = None
        self.last_report: Optional[TestReport] = None

    @pytest.hookimpl
    def pytest_sessionstart(self, session: Session) -> None:
        """
        Setup-class handler, signs in user, creates a testsuite,
        testcase, job and registers testrun in Zebrunner
        """

        self.event_loop.run_until_complete(self.api.auth())
        self.test_run_id = self.event_loop.run_until_complete(
            self.api.start_test_run(
                self.settings.zebrunner_project,
                StartTestRunModel(
                    name="test_run_name",
                    framework="pytest",
                    config=TestRunConfigModel(environment=self.settings.env, suite=self.settings.suite),
                ),
            )
        )

    @pytest.hookimpl
    def pytest_sessionfinish(self, session: Session, exitstatus: Union[int, ExitCode]) -> None:
        if not self.test_run_id:
            return

        self.event_loop.run_until_complete(self.api.finish_test_run(self.test_run_id))
        self.event_loop.run_until_complete(self.api.close())

    @pytest.hookimpl
    def pytest_runtest_makereport(self, item: Item, call: CallInfo) -> TestReport:
        report = TestReport.from_item_and_call(item, call)
        report.item = item
        return report

    @pytest.hookimpl
    def pytest_runtest_logreport(self, report: TestReport) -> None:
        if report.when != "setup" and not self.last_report:
            return

        if report.when == "setup":
            self.setup_test(report)
        elif report.when == "call":
            self.call_test(report)
        elif report.when == "teardown":
            self.teardown_test(report)
        else:
            print("Unable to finish test properly")

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
        self.last_report = report

    def call_test(self, report: TestReport) -> None:
        if not self.test_id or not self.test_run_id:
            return

        driver = DriverInfo()
        if driver.info is not None:
            logger.info(driver.info)

        if report.passed:
            status = TestStatus.PASSED
        else:
            status = TestStatus.FAILED

        self.event_loop.run_until_complete(
            self.api.finish_test(self.test_run_id, self.test_id, FinishTestModel(result=status.value))
        )
        self.last_report = report

    def teardown_test(self, report: TestReport) -> None:
        if not self.test_id or not self.test_run_id or not self.last_report:
            return

        if report.when == "teardown" and self.last_report.when == "setup":
            self.event_loop.run_until_complete(
                self.api.finish_test(self.test_run_id, self.test_id, FinishTestModel(result=TestStatus.SKIPPED.value))
            )
        self.last_report = None
