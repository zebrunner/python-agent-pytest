import logging
from typing import Union

import pytest
from _pytest.config import Config, ExitCode
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo

from pytest_zebrunner.api.client import ZebrunnerAPI
from pytest_zebrunner.api.models import (
    FinishTestModel,
    StartTestModel,
    StartTestRunModel,
    TestRunConfigModel,
    TestStatus,
)
from pytest_zebrunner.context import Test, TestRun, zebrunner_context
from pytest_zebrunner.selenium_integration import SeleniumSession, inject_driver
from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler

logger = logging.getLogger(__name__)


class PytestZebrunnerHooks:
    def __init__(self) -> None:
        self.api = ZebrunnerAPI(zebrunner_context.settings.service_url, zebrunner_context.settings.access_token)
        self.session_manager = SeleniumSession(self.api)

    @pytest.hookimpl
    def pytest_sessionstart(self, session: Session) -> None:
        self.api.auth()
        inject_driver(self.session_manager)
        settings = zebrunner_context.settings
        test_run = TestRun(settings.test_run_name, settings.env, settings.build)

        zebrunner_context.test_run = test_run
        test_run.zebrunner_id = self.api.start_test_run(
            settings.zebrunner_project,
            StartTestRunModel(
                name=test_run.name,
                framework="pytest",
                config=TestRunConfigModel(environment=test_run.environment, build=test_run.build),
            ),
        )
        logging.root.addHandler(ZebrunnerHandler())

    @pytest.hookimpl
    def pytest_sessionfinish(self, session: Session, exitstatus: Union[int, ExitCode]) -> None:
        if zebrunner_context.test_run_is_active:
            self.api.finish_test_run(zebrunner_context.test_run_id)
            self.session_manager.finish_all_sessions()

            handlers = list(filter(lambda x: isinstance(x, ZebrunnerHandler), logging.root.handlers))
            if len(handlers) > 0:
                zebrunner_handler: ZebrunnerHandler = handlers[0]  # type: ignore
                zebrunner_handler.push_logs()

        self.api.close()

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
        test_item: Item = report.item
        test = Test(
            name=test_item.name,
            file=test_item.nodeid.split("::")[1],
            maintainers=[mark.args[0] for mark in test_item.iter_markers("maintainer")],
            labels=[(str(mark.args[0]), str(mark.args[1])) for mark in test_item.iter_markers("label")],
        )
        zebrunner_context.test = test

        if zebrunner_context.test_run_is_active:
            test.zebrunner_id = self.api.start_test(
                zebrunner_context.test_run_id,
                StartTestModel(
                    name=test.name,
                    class_name=test.file,
                    method_name=test.name,
                    maintainer=",".join(test.maintainers),
                    labels=[{"key": label[0], "value": label[1]} for label in test.labels],
                ),
            )
            self.session_manager.add_test(zebrunner_context.test_id)

        if report.skipped and zebrunner_context.test_is_active:
            skip_markers = list(filter(lambda x: x.name == "skip", report.item.own_markers))
            skip_reason = skip_markers[0].kwargs.get("reason") if skip_markers else None
            self.api.finish_test(
                zebrunner_context.test_run_id,
                zebrunner_context.test_id,
                FinishTestModel(reason=skip_reason, result=TestStatus.SKIPPED.value),
            )
            zebrunner_context.test = None

    def call_test(self, report: TestReport) -> None:
        if zebrunner_context.test_is_active:
            if report.skipped:
                self.api.finish_test(
                    zebrunner_context.test_run_id,
                    zebrunner_context.test_id,
                    FinishTestModel(result=TestStatus.SKIPPED.value, reason=report.wasxfail or None),
                )
                zebrunner_context.test = None
                return

            if report.passed:
                status = TestStatus.PASSED
            else:
                status = TestStatus.FAILED

            body = FinishTestModel(result=status.value)
            self.api.finish_test(zebrunner_context.test_run_id, zebrunner_context.test_id, body)
