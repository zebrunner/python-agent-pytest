import logging
from typing import List, Optional

from _pytest._code.code import ExceptionChainRepr, ReprExceptionInfo
from _pytest.nodes import Item
from _pytest.reports import TestReport

from pytest_zebrunner.api.client import ZebrunnerAPI
from pytest_zebrunner.api.models import (
    ArtifactReferenceModel,
    CorrelationDataModel,
    FinishTestModel,
    FinishTestSessionModel,
    MilestoneModel,
    NotificationsType,
    NotificationTargetModel,
    StartTestModel,
    StartTestRunModel,
    StartTestSessionModel,
    TestRunConfigModel,
    TestStatus,
)
from pytest_zebrunner.ci_loaders import resolve_ci_context
from pytest_zebrunner.context import Test, TestRun, zebrunner_context
from pytest_zebrunner.zebrunner_logging import ZebrunnerHandler

logger = logging.getLogger(__name__)


class ReportingService:
    def __init__(self) -> None:
        self.api = ZebrunnerAPI(
            zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token
        )

    def authorize(self) -> None:
        if not self.api.authenticated:
            self.api.auth()

    def get_notification_configurations(self) -> Optional[List[NotificationTargetModel]]:
        settings = zebrunner_context.settings
        if settings.notifications:
            configs = []
            if settings.notifications.emails:
                configs.append(
                    NotificationTargetModel(
                        type=NotificationsType.EMAIL_RECIPIENTS.value, value=settings.notifications.emails
                    )
                )
            if settings.notifications.slack_channels:
                configs.append(
                    NotificationTargetModel(
                        type=NotificationsType.SLACK_CHANNELS.value, value=settings.notifications.slack_channels
                    )
                )
            if settings.notifications.ms_teams_channels:
                configs.append(
                    NotificationTargetModel(
                        type=NotificationsType.MS_TEAMS_CHANNELS.value, value=settings.notifications.ms_teams_channels
                    )
                )
            return configs
        else:
            return None

    def start_test_run(self) -> None:
        self.authorize()
        settings = zebrunner_context.settings
        test_run = TestRun(settings.run.display_name, settings.run.environment, settings.run.build)
        zebrunner_context.test_run = test_run
        milestone = (
            MilestoneModel(id=settings.milestone.id, name=settings.milestone.name) if settings.milestone else None
        )
        test_run.zebrunner_id = self.api.start_test_run(
            settings.project_key,
            StartTestRunModel(
                name=test_run.name,
                framework="pytest",
                config=TestRunConfigModel(environment=test_run.environment, build=test_run.build),
                milestone=milestone,
                ci_context=resolve_ci_context(),
                notification_targets=self.get_notification_configurations(),
            ),
        )

    def start_test(self, report: TestReport) -> None:
        self.authorize()
        test = Test(
            name=report.nodeid.split("::")[1],
            file=report.nodeid.split("::")[0],
            maintainers=report.maintainers,
            labels=report.labels,
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
                    correlation_data=CorrelationDataModel(name=test.name).json(),
                ),
            )

            if report.artifact_references:
                references = [ArtifactReferenceModel(name=x[0], value=x[1]) for x in report.artifact_references]
                self.api.send_artifact_references(references, zebrunner_context.test_run_id, zebrunner_context.test_id)
            if report.artifacts:
                for artifact in report.artifacts:
                    self.api.send_artifact(artifact, zebrunner_context.test_run_id, zebrunner_context.test_id)

    def finish_test(self, report: TestReport) -> None:
        if zebrunner_context.test_is_active:
            self.authorize()
            is_skip = report.when == "setup" and report.outcome == "skipped"
            is_xfail = hasattr(report, "wasxfail")

            reason = None
            if report.passed:
                status = TestStatus.PASSED
            elif is_skip or is_xfail:
                status = TestStatus.SKIPPED
            else:
                status = TestStatus.FAILED

            if is_xfail:
                reason = report.wasxfail
            elif is_skip:
                reason = report.longrepr[-1] if isinstance(report.longrepr, tuple) else str(report.longrepr)
            else:
                # Following this changelog check if it's string or ReprExceptionInfo
                # https://docs.pytest.org/en/6.2.x/changelog.html?highlight=reprexceptioninfo#pytest-6-0-0rc1-2020-07-08
                reason = str(report.longrepr)
                if isinstance(report.longrepr, ReprExceptionInfo) or isinstance(report.longrepr, ExceptionChainRepr):
                    reason = report.longrepr.reprcrash.message + "\n\n" + reason

            self.api.finish_test(
                zebrunner_context.test_run_id,
                zebrunner_context.test_id,
                FinishTestModel(
                    result=status.value,
                    reason=reason,
                ),
            )
            zebrunner_context.test = None

    def finish_test_run(self) -> None:
        self.authorize()
        if zebrunner_context.test_run_is_active:
            self.api.finish_test_run(zebrunner_context.test_run_id)

            handlers = list(filter(lambda x: isinstance(x, ZebrunnerHandler), logging.root.handlers))
            if len(handlers) > 0:
                zebrunner_handler: ZebrunnerHandler = handlers[0]  # type: ignore
                zebrunner_handler.push_logs()

        self.api.close()

    def start_test_session(
        self, session_id: str, capabilities: dict, desired_capabilities: dict, test_ids: List[int]
    ) -> Optional[str]:
        self.authorize()
        if zebrunner_context.test_run_is_active:
            zebrunner_session_id = self.api.start_test_session(
                zebrunner_context.test_run_id,
                StartTestSessionModel(
                    session_id=session_id,
                    desired_capabilities=desired_capabilities,
                    capabilities=capabilities,
                    test_ids=test_ids,
                ),
            )
            return zebrunner_session_id
        return None

    def finish_test_session(self, zebrunner_session_id: str, related_tests: List[str]) -> None:
        self.authorize()
        if zebrunner_context.test_run_is_active:
            self.api.finish_test_session(
                zebrunner_context.test_run_id,
                zebrunner_session_id,
                FinishTestSessionModel(test_ids=related_tests),
            )

    def filter_test_items(self, items: List[Item]) -> List[Item]:
        run_context = zebrunner_context.settings.run.context
        if run_context is not None:
            self.authorize()
            context_data = self.api.get_rerun_tests(run_context)
            rerun_names = {x.correlation_data.name for x in context_data.tests if x.correlation_data is not None}
            return list(filter(lambda x: x.name in rerun_names, items)) if rerun_names else items
        else:
            return items
