from pytest_zebrunner.tcm.base import BaseTcm


class Zebrunner(BaseTcm):
    _SYNC_ENABLED = "com.zebrunner.app/tcm.zebrunner.sync.enabled"
    _SYNC_REAL_TIME = "com.zebrunner.app/tcm.zebrunner.sync.real-time"
    _RUN_ID = "com.zebrunner.app/tcm.zebrunner.test-run-id"
    _CASE_ID = "com.zebrunner.app/tcm.zebrunner.test-case-key"

    @staticmethod
    def disable_sync() -> None:
        Zebrunner._verify_no_tests()
        Zebrunner._attach_label(Zebrunner._SYNC_ENABLED, "false")

    @staticmethod
    def enable_real_time_sync() -> None:
        Zebrunner._verify_no_tests()
        Zebrunner._attach_label(Zebrunner._SYNC_REAL_TIME, "true")

    @staticmethod
    def set_run_id(run_id: str) -> None:
        Zebrunner._verify_no_tests()
        Zebrunner._attach_label(Zebrunner._RUN_ID, run_id)

    @staticmethod
    def set_test_case_key(test_case_key: str) -> None:
        Zebrunner._attach_label(Zebrunner._CASE_ID, test_case_key)
