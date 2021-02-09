import logging
from datetime import datetime
from typing import Optional, Union

import pytest
from _pytest.config import Config, ExitCode
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo

from pytest_zebrunner.context import ZebrunnerContext
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
from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler

logger = logging.getLogger(__name__)


class PytestZebrunnerHooks:
    def __init__(self, settings: ZebrunnerSettings, context: ZebrunnerContext):
        self.settings = settings
        self.api = ZebrunnerAPI(self.settings.service_url, self.settings.access_token)
        self.session_manager = SeleniumSession(self.api)

        self.zebrunner_context = context

    @pytest.hookimpl
    def pytest_sessionstart(self, session: Session) -> None:
        self.api.auth()
        inject_driver(self.session_manager)

        self.zebrunner_context.test_run_id = self.api.start_test_run(
            self.settings.zebrunner_project,
            StartTestRunModel(
                name=self.settings.test_run_name or f"Unnamed {datetime.utcnow()}",
                framework="pytest",
                config=TestRunConfigModel(environment=self.settings.env, build=self.settings.build),
            ),
        )
        logging.root.addHandler(ZebrunnerHandler())

    @pytest.hookimpl
    def pytest_sessionfinish(self, session: Session, exitstatus: Union[int, ExitCode]) -> None:
        if not self.zebrunner_context.test_run_id:
            return

        self.api.finish_test_run(self.zebrunner_context.test_run_id)
        self.session_manager.finish_all_sessions()

        handlers = list(filter(lambda x: isinstance(x, ZebrunnerHandler), logging.root.handlers))
        zebrunner_handler: Optional[ZebrunnerHandler] = handlers[0] if handlers else None  # type: ignore
        if zebrunner_handler:
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
        if not self.zebrunner_context.test_run_id:
            return

        test_item: Item = report.item

        test_name = test_item.name
        class_name = test_item.nodeid.split("::")[1]
        maintainer = ",".join([mark.args[0] for mark in test_item.iter_markers("maintainer")])
        labels = [mark.args[0] for mark in test_item.iter_markers("labels")]
        if labels:
            labels = labels[0]

        self.zebrunner_context.test_id = self.api.start_test(
            self.zebrunner_context.test_run_id,
            StartTestModel(
                name=test_name,
                class_name=class_name,
                method_name=test_name,
                maintainer=maintainer or None,
                labels=[{"key": label[0], "value": label[1]} for label in labels],
            ),
        )

        if report.skipped and self.zebrunner_context.test_id:
            skip_markers = list(filter(lambda x: x.name == "skip", report.item.own_markers))
            skip_reason = skip_markers[0].kwargs.get("reason") if skip_markers else None
            self.api.finish_test(
                self.zebrunner_context.test_run_id,
                self.zebrunner_context.test_id,
                FinishTestModel(reason=skip_reason, result=TestStatus.SKIPPED.value),
            )
            self.zebrunner_context.test_id = None
            return

        self.session_manager.add_test(str(self.zebrunner_context.test_id))

    def call_test(self, report: TestReport) -> None:
        if not self.zebrunner_context.test_id or not self.zebrunner_context.test_run_id:
            return

        if report.skipped:
            self.api.finish_test(
                self.zebrunner_context.test_run_id,
                self.zebrunner_context.test_id,
                FinishTestModel(result=TestStatus.SKIPPED.value, reason=report.wasxfail or None),
            )
            self.zebrunner_context.test_id = None
            return

        if report.passed:
            status = TestStatus.PASSED
        else:
            status = TestStatus.FAILED

        finish_test_data = FinishTestModel(result=status.value)
        self.api.finish_test(self.zebrunner_context.test_run_id, self.zebrunner_context.test_id, finish_test_data)
