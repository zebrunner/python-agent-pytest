import datetime
import time
from copy import deepcopy
from logging import LogRecord
from typing import Any, Dict

from requests import Response

from .api_request import APIRequest
from .context import Context, Parameter
from .resources import refresh_token, test_log, test_result_v1, test_run_v1, test_v1


class ZafiraClient:

    TEST_RUNS_PATH_V1 = "/api/reporting/v1/test-runs?projectKey={}"
    REFRESH_TOKEN_PATH = "/api/iam/v1/auth/refresh"
    TESTS_PATH_V1 = "/api/reporting/v1/test-runs/{}/tests"
    TESTS_FINISH_PATH_V1 = "/api/reporting/v1/test-runs/{}/tests/{}"
    TEST_RUNS_FINISH_PATH_V1 = "/api/reporting/v1/test-runs/{}"
    TEST_LOGS_PATH = "/api/reporting/v1/test-runs/{}/logs"
    TEST_SCREENSHOTS_PATH = "/api/reporting/v1/test-runs/{}/tests/{}/screenshots"
    TEST_RUN_ARTIFACT_V1 = "/api/reporting/v1/test-runs/{}/tests/{}/artifacts"

    INSTANCE = None

    def __new__(cls, service_url: str) -> "ZafiraClient":
        if not cls.INSTANCE:
            cls.INSTANCE = super(ZafiraClient, cls).__new__(cls)
        return cls.INSTANCE

    def __init__(self, service_url: str) -> None:
        self.api = APIRequest(service_url)
        self.auth_token = ""

    def start_test_run(self, started_at: datetime.datetime, framework: str, project: str) -> Response:
        body = deepcopy(test_run_v1)
        body["name"] = Context.get(Parameter.SUITE)
        started_at = started_at.replace(tzinfo=datetime.timezone.utc)
        body["startedAt"] = started_at.isoformat()
        body["framework"] = framework
        config = body["config"]
        config["env"] = Context.get(Parameter.ENV)  # noqa
        config["appVersion"] = Context.get(Parameter.BUILD)  # noqa
        return self.api.send_post(
            ZafiraClient.TEST_RUNS_PATH_V1.format(project),
            body,
            headers=self.init_auth_headers(),
            default_err_msg="Unable to start test run",
        )

    def finish_test_run(self, test_run: Dict) -> Response:
        test_run["endedAt"] = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        return self.api.send_put(
            ZafiraClient.TEST_RUNS_FINISH_PATH_V1.format(test_run["id"]),
            test_run,
            headers=self.init_auth_headers(),
            default_err_msg="Unable to finish test run",
        )

    def start_test(
        self,
        uid: str,
        test_run_id: str,
        test_name: str,
        maintainer: str,
        started_at: datetime.datetime,
        class_name: str,
    ) -> Response:
        body = deepcopy(test_v1)
        body["uuid"] = uid
        body["name"] = test_name
        body["maintainer"] = maintainer
        started_at = started_at.replace(tzinfo=datetime.timezone.utc)
        body["startedAt"] = started_at.isoformat()
        body["className"] = class_name
        return self.api.send_post(
            ZafiraClient.TESTS_PATH_V1.format(test_run_id),
            body,
            headers=self.init_auth_headers(),
            default_err_msg="Unable to start test",
        )

    def finish_test(self, test_run_id: str, test_id: str, test: Dict) -> Response:
        body = deepcopy(test_result_v1)
        body["id"] = test_id
        body["uuid"] = test["uuid"]
        body["name"] = test["name"]
        body["startedAt"] = test["startedAt"]
        body["className"] = test["className"]
        body["methodName"] = test["methodName"]
        body["result"] = test["result"]
        body["reason"] = test.get("reason") or "passed"
        body["endedAt"] = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        return self.api.send_put(
            ZafiraClient.TESTS_FINISH_PATH_V1.format(test_run_id, test_id),
            body,
            headers=self.init_auth_headers(),
            default_err_msg="Unable to finish test",
        )

    def push_log_record(self, test_run_id: str, test_id: str, record: LogRecord) -> Response:
        body = deepcopy(test_log)
        list_entry = {
            "testId": test_id,
            "level": record.levelname,
            "timestamp": time.time() * 1000,
            "message": record.msg,
        }
        body.append(list_entry)
        return self.api.send_post(
            ZafiraClient.TEST_LOGS_PATH.format(test_run_id),
            body,
            headers=self.init_auth_headers(),
            default_err_msg="Unable to send log entry",
        )

    def push_screenshot(self, test_run_id: str, test_id: str, image: Any) -> Response:
        return self.api.send_post_screenshot(
            ZafiraClient.TEST_SCREENSHOTS_PATH.format(test_run_id, test_id),
            image,
            headers=self.init_auth_headers_with_screenshot(),
            default_err_msg="Unable to send screenshot",
        )

    def push_artifact(self, test_run_id: str, test_id: str) -> Response:
        files = {"file": open(Context.get(Parameter.TEST_RUN_ARTIFACT), "rb")}
        return self.api.send_post_artifact(
            ZafiraClient.TEST_RUN_ARTIFACT_V1.format(test_run_id, test_id),
            files,
            headers=self.init_auth_headers(),
            default_err_msg="Unable to attach test artifact",
        )

    def refresh_token(self, token: str) -> Response:
        refresh_token["refreshToken"] = token
        return self.api.send_post_without_authorization(
            ZafiraClient.REFRESH_TOKEN_PATH, refresh_token, default_err_msg="Unable to refresh token"
        )

    def init_auth_headers(self) -> Dict[str, str]:
        return {"Authorization": "Bearer " + self.auth_token}

    def init_auth_headers_with_screenshot(self) -> Dict[str, str]:
        return {"Content-type": "image/png", "Authorization": "Bearer " + self.auth_token}


client = ZafiraClient(Context.get(Parameter.SERVICE_URL))
