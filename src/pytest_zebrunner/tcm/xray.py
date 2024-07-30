from pytest_zebrunner.tcm.base import BaseTcm


class Xray(BaseTcm):
    _SYNC_ENABLED = "com.zebrunner.app/tcm.xray.sync.enabled"
    _SYNC_REAL_TIME = "com.zebrunner.app/tcm.xray.sync.real-time"
    _EXECUTION_KEY = "com.zebrunner.app/tcm.xray.test-execution-key"
    _TEST_KEY = "com.zebrunner.app/tcm.xray.test-key"

    @staticmethod
    def disable_sync() -> None:
        Xray._verify_no_tests()
        Xray._attach_label(Xray._SYNC_ENABLED, "false")

    @staticmethod
    def enable_real_time_sync() -> None:
        Xray._verify_no_tests()
        Xray._attach_label(Xray._SYNC_REAL_TIME, "true")

    @staticmethod
    def set_execution_key(execution_key: str) -> None:
        Xray._verify_no_tests()
        Xray._attach_label(Xray._EXECUTION_KEY, execution_key)

    @staticmethod
    def set_test_key(test_key: str) -> None:
        Xray._attach_label(Xray._TEST_KEY, test_key)
