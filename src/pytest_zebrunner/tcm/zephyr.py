from pytest_zebrunner.tcm.base import BaseTcm


class Zephyr(BaseTcm):
    _SYNC_ENABLED = "com.zebrunner.app/tcm.zephyr.sync.enabled"
    _SYNC_REAL_TIME = "com.zebrunner.app/tcm.zephyr.sync.real-time"
    _TEST_CYCLE_KEY = "com.zebrunner.app/tcm.zephyr.test-cycle-key"
    _JIRA_PROJECT_KEY = "com.zebrunner.app/tcm.zephyr.jira-project-key"
    _TEST_CASE_KEY = "com.zebrunner.app/tcm.zephyr.test-case-key"

    @staticmethod
    def disable_sync() -> None:
        Zephyr._verify_no_tests()
        Zephyr._attach_label(Zephyr._SYNC_ENABLED, "false")

    @staticmethod
    def enable_real_time_sync() -> None:
        Zephyr._verify_no_tests()
        Zephyr._attach_label(Zephyr._SYNC_REAL_TIME, "true")

    @staticmethod
    def set_test_cycle_key(key: str) -> None:
        Zephyr._verify_no_tests()
        Zephyr._attach_label(Zephyr._TEST_CYCLE_KEY, key)

    @staticmethod
    def set_jira_project_key(key: str) -> None:
        Zephyr._verify_no_tests()
        Zephyr._attach_label(Zephyr._JIRA_PROJECT_KEY, key)

    @staticmethod
    def set_test_case_key(key: str) -> None:
        Zephyr._attach_label(Zephyr._TEST_CASE_KEY, key)
