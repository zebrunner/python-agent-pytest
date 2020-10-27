import datetime
import logging
import uuid
from typing import Any, Dict, List, Union

import pytest
from _pytest.config import ExitCode
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.runner import CallInfo

from .context import Context, Parameter
from .resource_constants import TestStatus
from .zafira_state import ZafiraState

# TODO Fix all mypy ignores and Any types


class BaseZafiraListener:

    LOGGER = logging.getLogger("zebrunner")

    def __init__(self, state: ZafiraState) -> None:
        self.state = state
        self.initialized = self.initialize_zafira()

    def initialize_zafira(self) -> bool:
        enabled = False
        try:
            self.state.refresh_token = self.state.zc.refresh_token(self.state.access_token).json()
            if self.state.refresh_token:
                self.state.zc.auth_token = self.state.refresh_token["authToken"]
            self.LOGGER.info("Zafira is " + "available" if self.state.is_enabled else "unavailable")
            enabled = self.state.is_enabled
        except Exception as e:
            self.LOGGER.error("Unable to initialize connector: {}".format(e))
        return enabled

    def compose_package_name(self, path_entries_list: List) -> str:
        if len(path_entries_list) == 2:
            return path_entries_list[0]
        return path_entries_list[0] + "/" + self.compose_package_name(path_entries_list[1:])

    def add_artifact_to_test(
        self, test: Dict, artifact_name: str, artifact_link: str, expires_in: datetime.datetime = None
    ) -> None:
        """
        Adds test artifact to test
        """
        try:
            self.state.zc.add_test_artifact_to_test(  # type: ignore
                test["id"], artifact_link, artifact_name, expires_in
            )
        except Exception as e:
            self.LOGGER.error("Unable to add artifact to test correctly: {}".format(e))

    def on_test_success(self) -> None:
        """
        An abstract handler for posting successfull test onto Zafira UI
        """

    def on_test_failure(self, message: str) -> None:
        """
        An abstract handler for posting failed test onto Zafira UI
        :param message: error message from failing test
        """

    def on_test_skipped(self, message: str) -> None:
        """
        An abstract handler for posting skipped test onto Zafira UI
        :param message: skip reason
        """

    def add_work_item_to_test(self, test_id: str, work_item: list) -> None:
        if not self.state.is_enabled:
            return
        try:
            work_items = list()
            work_items.append(work_item if len(work_item) < self.state.MAX_LENGTH_OF_WORKITEM else "Skipped")
            self.state.zc.create_test_work_items(test_id, work_items)  # type: ignore
        except Exception as e:
            self.LOGGER.error("Unable to add work item: {}".format(e))


class PyTestZafiraListener(BaseZafiraListener):
    """
    Contains hook implementations
    """

    FRAMEWORK = "pytest"

    def __init__(self, state: ZafiraState) -> None:
        super().__init__(state)

    @pytest.hookimpl
    def pytest_sessionstart(self, session: Session) -> None:
        """
        Setup-class handler, signs in user, creates a testsuite,
        testcase, job and registers testrun in Zafira
        """
        if not self.initialized:
            return
        try:
            self.state.test_run = self.state.zc.start_test_run(
                datetime.datetime.utcnow(), self.FRAMEWORK, self.state.zafira_project
            ).json()
            self.state.test_run_id = self.state.test_run["id"]  # type: ignore
        except Exception as e:
            self.state.is_enabled = False
            self.LOGGER.error("Undefined error during test run registration! {}".format(e))

    @pytest.hookimpl
    def pytest_runtest_setup(self, item: Item) -> None:
        """
        Setup handler, set up initial parameters for test,
        attaches to testsuite, registers and starts the test
        """
        if not self.state.is_enabled:
            return
        try:
            test_name = item.name
            class_name = item.nodeid.split("::")[1]
            uid = str(uuid.uuid4())
            maintainer = [
                marker for marker in item.own_markers if marker.name in Context.get_list(Parameter.TEST_OWNERS)
            ]
            maintainer = "anonymous" if len(maintainer) == 0 else maintainer[0].name
            # fmt: off
            self.state.test = self.state.zc.start_test(
                uid,
                self.state.test_run_id,  # type: ignore
                test_name,
                maintainer,  # type: ignore
                datetime.datetime.utcnow(),
                class_name
            ).json()
            # fmt: on
            self.state.test_id = self.state.test["id"]  # type: ignore
            self.state.zc.push_artifact(self.state.test_run_id, self.state.test_id)  # type: ignore
        except Exception as e:
            self.LOGGER.error("Undefined error during test case/method start! {}".format(e))

    @pytest.hookimpl
    def pytest_runtest_teardown(self, item: Any) -> None:
        """
        Teardown handler. Finishes test, adds workitems if needed
        """
        if not self.state.is_enabled:
            return
        try:
            skip_mark = [marker for marker in item.own_markers if marker.name == "skip"]
            if skip_mark:
                test_name = item.name
                class_name = item.nodeid.split("::")[1]
                uid = str(uuid.uuid4())
                maintainer = [
                    marker for marker in item.own_markers if marker.name in Context.get_list(Parameter.TEST_OWNERS)
                ]
                maintainer = "anonymous" if len(maintainer) == 0 else maintainer[0].name
                # fmt: off
                self.state.test = self.state.zc.start_test(
                    uid,
                    self.state.test_run_id,  # type: ignore
                    test_name,
                    maintainer,  # type: ignore
                    datetime.datetime.utcnow(),
                    class_name
                ).json()
                # fmt: on
                self.state.test_id = self.state.test["id"]  # type: ignore
                self.state.test["result"] = TestStatus.SKIPPED.value  # type: ignore
                self.state.test["reason"] = skip_mark[0].kwargs["reason"]  # type: ignore

            self.state.zc.finish_test(self.state.test_run_id, self.state.test_id, self.state.test)  # type: ignore
        except Exception as e:
            self.LOGGER.error("Unable to finish test run correctly: {}".format(e))

    @pytest.hookimpl
    def pytest_runtest_logreport(self, report: Any) -> None:
        """
        Set test status, stacktrace if needed
        :param report: info about test
        """
        if not self.state.is_enabled:
            return
        try:
            if report.when == "setup":
                if report.failed:
                    self.on_test_failure(report)
            if report.when == "call":
                test_result = report.outcome
                if test_result == "passed":
                    self.on_test_success()
                elif test_result == "failed":
                    self.on_test_failure(report)
                else:
                    self.on_test_skipped(report)

        except Exception as e:
            self.LOGGER.error("Unable to finish test correctly: {}".format(e))

    @pytest.hookimpl
    def pytest_sessionfinish(self, session: Session, exitstatus: Union[int, ExitCode]) -> None:
        """
        Teardown-class handler, closes the testrun
        """
        if not self.state.is_enabled:
            return
        try:
            if self.state.test_run is not None:
                self.state.zc.finish_test_run(self.state.test_run.json())
        except Exception as e:
            self.LOGGER.error("Unable to finish test run correctly: {}".format(e))

    @pytest.hookimpl
    def pytest_runtest_makereport(self, item: Item, call: CallInfo) -> None:
        if not self.on_exception(item, call):
            return

        self.LOGGER.debug("Exception occurs... " "Trying to catch screenshot")

        if self.state.test_run:
            test_run_id = self.state.test_run.json()["id"]
            test_id = self.state.test["id"]
            self.state.zc.push_screenshot(test_run_id, test_id, item.instance.driver.get_screenshot_as_png())

    @staticmethod
    def on_exception(item: Item, call: CallInfo) -> Any:
        return hasattr(item.instance, Context.get(Parameter.DRIVER_INSTANCE_NAME)) and call.excinfo

    def on_test_success(self) -> None:
        if self.state.test is not None:
            self.state.test["result"] = TestStatus.PASSED.value

    def on_test_failure(self, message: Any) -> None:
        if self.state.test is not None:
            self.state.test["result"] = TestStatus.FAILED.value
            self.state.test["reason"] = message.longreprtext

    def on_test_skipped(self, message: Any) -> None:
        if self.state.test is not None:
            if not hasattr(message, "wasxfail"):
                self.state.test["result"] = TestStatus.SKIPPED.value
                self.state.test["reason"] = message.longreprtext
            else:
                self.state.test["result"] = TestStatus.FAILED.value
                self.state.test["reason"] = message.wasxfail
