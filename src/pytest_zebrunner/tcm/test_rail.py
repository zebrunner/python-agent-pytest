from pytest_zebrunner.tcm.base import BaseTcm


class TestRail(BaseTcm):
    _SYNC_ENABLED = "com.zebrunner.app/tcm.testrail.sync.enabled"
    _SYNC_REAL_TIME = "com.zebrunner.app/tcm.testrail.sync.real-time"
    _INCLUDE_ALL = "com.zebrunner.app/tcm.testrail.include-all-cases"
    _SUITE_ID = "com.zebrunner.app/tcm.testrail.suite-id"
    _RUN_ID = "com.zebrunner.app/tcm.testrail.run-id"
    _RUN_NAME = "com.zebrunner.app/tcm.testrail.run-name"
    _MILESTONE = "com.zebrunner.app/tcm.testrail.milestone"
    _ASSIGNEE = "com.zebrunner.app/tcm.testrail.assignee"
    _CASE_ID = "com.zebrunner.app/tcm.testrail.case-id"

    @staticmethod
    def disable_sync() -> None:
        TestRail._verify_no_tests()
        TestRail._attach_label(TestRail._SYNC_ENABLED, "false")

    @staticmethod
    def enable_real_time_sync() -> None:
        TestRail._verify_no_tests()
        TestRail._attach_label(TestRail._SYNC_REAL_TIME, "true")
        TestRail._attach_label(TestRail._INCLUDE_ALL, "true")

    @staticmethod
    def include_all_test_cases_in_new_run() -> None:
        TestRail._verify_no_tests()
        TestRail._attach_label(TestRail._INCLUDE_ALL, "true")

    @staticmethod
    def set_suite_id(suite_id: str) -> None:
        TestRail._verify_no_tests()
        TestRail._attach_label(TestRail._SUITE_ID, suite_id)

    @staticmethod
    def set_run_id(run_id: str) -> None:
        TestRail._verify_no_tests()
        TestRail._attach_label(TestRail._RUN_ID, run_id)

    @staticmethod
    def set_run_name(run_name: str) -> None:
        TestRail._verify_no_tests()
        TestRail._attach_label(TestRail._RUN_NAME, run_name)

    @staticmethod
    def set_milestone(milestone: str) -> None:
        TestRail._verify_no_tests()
        TestRail._attach_label(TestRail._MILESTONE, milestone)

    @staticmethod
    def set_assignee(assignee: str) -> None:
        TestRail._verify_no_tests()
        TestRail._attach_label(TestRail._ASSIGNEE, assignee)

    @staticmethod
    def set_case_id(test_case_id: str) -> None:
        TestRail._attach_label(TestRail._CASE_ID, test_case_id)
