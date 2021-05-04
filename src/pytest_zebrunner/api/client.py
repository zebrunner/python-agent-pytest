import json
import logging
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from pprint import pformat
from typing import List, Optional, Union

import httpx
from httpx import Client, Request, Response

from pytest_zebrunner.api.models import (
    ArtifactReferenceModel,
    FinishTestModel,
    FinishTestSessionModel,
    LabelModel,
    LogRecordModel,
    RerunDataModel,
    StartTestModel,
    StartTestRunModel,
    StartTestSessionModel,
)
from pytest_zebrunner.utils import Singleton

logger = logging.getLogger(__name__)


def log_response(response: Response, log_level: int = logging.DEBUG) -> None:
    request = response.request
    request.read()

    logger.log(
        log_level,
        f"Request {request.method} {request.url}\n"
        f"Headers: \n{pformat(dict(request.headers))}\n\n"
        f"Content: \n{request.content}\n\n"
        f"Response Code: {response.status_code}\n"
        f" Content: \n{pformat(response.json())}",
    )


class ZebrunnerAPI(metaclass=Singleton):
    authenticated = False

    def __init__(self, service_url: str = None, access_token: str = None):
        if service_url and access_token:
            self.service_url = service_url.rstrip("/")
            self.access_token = access_token
            self._client = Client()
            self._auth_token = None
            self.authenticated = False

    def _sign_request(self, request: Request) -> Request:
        request.headers["Authorization"] = f"Bearer {self._auth_token}"
        return request

    def auth(self) -> None:
        if not self.access_token or not self.service_url:
            return

        url = self.service_url + "/api/iam/v1/auth/refresh"
        try:
            response = self._client.post(url, json={"refreshToken": self.access_token})
        except httpx.RequestError as e:
            logger.warning("Error while sending request to zebrunner.", exc_info=e)
            return

        if response.status_code != 200:
            log_response(response, logging.ERROR)
            return

        self._auth_token = response.json()["authToken"]
        self._client.auth = self._sign_request
        self.authenticated = True

    def start_test_run(self, project_key: str, body: StartTestRunModel) -> Optional[int]:
        url = self.service_url + "/api/reporting/v1/test-runs"

        try:
            response = self._client.post(
                url, params={"projectKey": project_key}, json=body.dict(exclude_none=True, by_alias=True)
            )
        except httpx.RequestError as e:
            logger.warning("Error while sending request to zebrunner.", exc_info=e)
            return None

        if response.status_code != 200:
            log_response(response, logging.ERROR)
            return None

        return response.json()["id"]

    def start_test(self, test_run_id: int, body: StartTestModel) -> Optional[int]:
        url = self.service_url + f"/api/reporting/v1/test-runs/{test_run_id}/tests"

        try:
            response = self._client.post(url, json=body.dict(exclude_none=True, by_alias=True))
        except httpx.RequestError as e:
            logger.warning("Error while sending request to zebrunner.", exc_info=e)
            return None

        if response.status_code != 200:
            log_response(response, logging.ERROR)
            return None

        return response.json()["id"]

    def finish_test(self, test_run_id: int, test_id: int, body: FinishTestModel) -> None:
        url = self.service_url + f"/api/reporting/v1/test-runs/{test_run_id}/tests/{test_id}"

        try:
            response = self._client.put(url, json=body.dict(exclude_none=True, by_alias=True))
        except httpx.RequestError as e:
            logger.warning("Error while sending request to zebrunner.", exc_info=e)
            return

        if response.status_code != 200:
            log_response(response, logging.ERROR)

    def finish_test_run(self, test_run_id: int) -> None:
        url = self.service_url + f"/api/reporting/v1/test-runs/{test_run_id}"
        try:
            response = self._client.put(
                url,
                json={"endedAt": (datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(seconds=1)).isoformat()},
            )
        except httpx.RequestError as e:
            logger.warning("Error while sending request to zebrunner.", exc_info=e)
            return

        if response.status_code != 200:
            log_response(response, logging.ERROR)
            return

    def send_logs(self, test_run_id: int, logs: List[LogRecordModel]) -> None:
        url = self.service_url + f"/api/reporting/v1/test-runs/{test_run_id}/logs"

        body = [x.dict(exclude_none=True, by_alias=True) for x in logs]
        self._client.post(url, json=body)

    def send_screenshot(self, test_run_id: int, test_id: int, image_path: Union[str, Path]) -> None:
        url = self.service_url + f"/api/reporting/v1/test-runs/{test_run_id}/tests/{test_id}/screenshots"
        with open(image_path, "rb") as image:
            self._client.post(
                url,
                content=image.read(),
                headers={"Content-Type": "image/png", "x-zbr-screenshot-captured-at": round(time.time() * 1000)},
            )

    def send_artifact(self, filename: Union[str, Path], test_run_id: int, test_id: Optional[int] = None) -> None:
        if test_id:
            url = f"{self.service_url}/api/reporting/v1/test-runs/{test_run_id}/tests/{test_id}/artifacts"
        else:
            url = f"{self.service_url}/api/reporting/v1/test-runs/{test_run_id}/artifacts"
        with open(filename, "rb") as file:
            self._client.post(url, files={"file": file})

    def send_artifact_references(
        self, references: List[ArtifactReferenceModel], test_run_id: int, test_id: Optional[int] = None
    ) -> None:
        if test_id:
            url = f"{self.service_url}/api/reporting/v1/test-runs/{test_run_id}/tests/{test_id}/artifact-references"
        else:
            url = f"{self.service_url}/api/reporting/v1/test-runs/{test_run_id}/artifact-references/"
        json_items = [item.dict(exclude_none=True, by_alias=True) for item in references]
        self._client.put(url, json={"items": json_items})

    def send_labels(self, labels: List[LabelModel], test_run_id: int, test_id: Optional[int] = None) -> None:
        if test_id:
            url = f"{self.service_url}/api/reporting/v1/test-runs/{test_run_id}/tests/{test_id}/labels"
        else:
            url = f"{self.service_url}/api/reporting/v1/test-runs/{test_run_id}/labels"
        labels_json = [label.dict(exclude_none=True, by_alias=True) for label in labels]
        self._client.put(url, json={"items": labels_json})

    def start_test_session(self, test_run_id: int, body: StartTestSessionModel) -> Optional[str]:
        url = self.service_url + f"/api/reporting/v1/test-runs/{test_run_id}/test-sessions"
        response = self._client.post(url, json=body.dict(exclude_none=True, by_alias=True))
        if not response.status_code == 200:
            log_response(response, logging.ERROR)
            return None

        return response.json().get("id")

    def finish_test_session(self, test_run_id: int, zebrunner_id: str, body: FinishTestSessionModel) -> None:
        url = self.service_url + f"/api/reporting/v1/test-runs/{test_run_id}/test-sessions/{zebrunner_id}"
        self._client.put(url, json=body.dict(exclude_none=True, by_alias=True))

    def get_rerun_tests(self, run_context: str) -> RerunDataModel:
        url = self.service_url + "/api/reporting/v1/run-context-exchanges"
        run_context_dict = json.loads(run_context)
        response = self._client.post(url, json=run_context_dict)
        return RerunDataModel(**response.json())

    def close(self) -> None:
        self._client.close()
