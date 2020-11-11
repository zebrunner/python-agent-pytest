from asyncio import get_event_loop
from typing import Optional, Union

import pytest
from _pytest.config import ExitCode
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.reports import CollectReport, TestReport
from _pytest.runner import CallInfo

from pytest_zebrunner.settings import ZebrunnerSettings
from pytest_zebrunner.zebrunner_api.client import ZebrunnerAPI
from pytest_zebrunner.zebrunner_api.models import (
    FinishTestModel,
    StartTestModel,
    StartTestRunModel,
    TestStatus,
)


class PytestZebrunnerHooks:
    def __init__(self, settings: ZebrunnerSettings):
        self.event_loop = get_event_loop()
        self.settings = settings

        self.api = ZebrunnerAPI(self.settings.service_url, self.settings.access_token)

        self.test_run_id: Optional[int] = None
        self.test_id: Optional[int] = None

    @pytest.hookimpl
    def pytest_sessionstart(self, session: Session) -> None:
        """
        Setup-class handler, signs in user, creates a testsuite,
        testcase, job and registers testrun in Zebrunner
        """

        self.event_loop.run_until_complete(self.api.auth())
        self.test_run_id = self.event_loop.run_until_complete(
            self.api.start_test_run(
                self.settings.zebrunner_project, StartTestRunModel(name="test_run_name", framework="pytest")
            )
        )

    @pytest.hookimpl
    def pytest_sessionfinish(self, session: Session, exitstatus: Union[int, ExitCode]) -> None:
        if not self.test_run_id:
            return

        self.event_loop.run_until_complete(self.api.finish_test_run(self.test_run_id))
        self.event_loop.run_until_complete(self.api.close())

    @pytest.hookimpl
    def pytest_runtest_setup(self, item: Item) -> None:
        """
        Setup handler, set up initial parameters for test,
        attaches to testsuite, registers and starts the test
        """
        if not self.test_run_id:
            return

        test_name = item.name
        class_name = item.nodeid.split("::")[1]
        # maintainer = [mark.args[0] for mark in item.iter_markers("maintainer")]

        self.test_id = self.event_loop.run_until_complete(
            self.api.start_test(
                self.test_run_id,
                StartTestModel(
                    name=test_name,
                    class_name=class_name,
                    method_name=item.name,
                    # maintainer=str(maintainer) if maintainer else None,
                ),
            )
        )

    @pytest.hookimpl
    def pytest_runtest_teardown(self, item: Item) -> None:
        if not self.test_id or not self.test_run_id:
            return

        class_name = item.nodeid.split("::")[1]

        test_id = self.event_loop.run_until_complete(
            self.api.start_test(
                self.test_run_id, StartTestModel(name=item.name, class_name=class_name, method_name=item.name)
            )
        )
        self.event_loop.run_until_complete(
            self.api.finish_test(self.test_run_id, test_id, FinishTestModel(result=TestStatus.IN_PROGRESS.value))
        )

    @pytest.hookimpl
    def pytest_runtest_logreport(self, report: Union[TestReport, CollectReport]) -> None:
        pass

    @pytest.hookimpl
    def pytest_runtest_makereport(self, item: Item, call: CallInfo) -> None:
        pass
