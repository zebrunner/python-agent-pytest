import logging
from datetime import datetime, timezone
from pprint import pformat
from typing import List

from httpx import AsyncClient, Request, Response

from pytest_zebrunner.zebrunner_api.models import (
    FinishTestModel,
    LogRecordModel,
    StartTestModel,
    StartTestRunModel,
)

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


class ZebrunnerAPI:
    def __init__(self, service_url: str, access_token: str):
        self.service_url = service_url.rstrip("/")
        self.access_token = access_token
        self._client = AsyncClient()
        self._auth_token = None

    def _sign_request(self, request: Request) -> Request:
        request.headers["Authorization"] = f"Bearer {self._auth_token}"
        return request

    async def auth(self) -> None:
        url = self.service_url + "/api/iam/v1/auth/refresh"
        response = await self._client.post(url, json={"refreshToken": self.access_token})
        if response.status_code != 200:
            log_response(response, logging.ERROR)
        self._auth_token = response.json()["authToken"]
        self._client.auth = self._sign_request

    async def start_test_run(self, project_key: str, body: StartTestRunModel) -> int:
        url = self.service_url + "/api/reporting/v1/test-runs"

        response = await self._client.post(
            url, params={"projectKey": project_key}, json=body.dict(exclude_none=True, by_alias=True)
        )
        if response.status_code != 200:
            log_response(response, logging.ERROR)

        return response.json()["id"]

    async def start_test(self, test_run_id: int, body: StartTestModel) -> int:
        url = self.service_url + f"/api/reporting/v1/test-runs/{test_run_id}/tests"

        response = await self._client.post(url, json=body.dict(exclude_none=True, by_alias=True))
        if response.status_code != 200:
            log_response(response, logging.ERROR)

        return response.json()["id"]

    async def finish_test(self, test_run_id: int, test_id: int, body: FinishTestModel) -> None:
        url = self.service_url + f"/api/reporting/v1/test-runs/{test_run_id}/tests/{test_id}"

        response = await self._client.put(url, json=body.dict(exclude_none=True, by_alias=True))
        if response.status_code != 200:
            log_response(response, logging.ERROR)

    async def finish_test_run(self, test_run_id: int) -> None:
        url = self.service_url + f"/api/reporting/v1/test-runs/{test_run_id}"

        response = await self._client.put(
            url, json={"endedAt": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()}
        )
        if response.status_code != 200:
            log_response(response, logging.ERROR)
            return

    async def send_logs(self, test_run_id: int, logs: List[LogRecordModel]) -> None:
        # url = self.service_url + f"/api/reporting/v1/test-runs/{test_run_id}/logs"

        raise NotImplementedError

    async def send_screenshot(self, test_run_id: int, test_id: int) -> None:
        # url = self.service_url + f"/api/reporting/v1/test-runs/{test_run_id}/tests/{test_id}/screenshots"

        raise NotImplementedError

    async def send_artifact(self, test_run_id: int) -> None:
        # url = self.service_url + f"/api/reporting/v1/test-runs/{test_run_id}/artifact-refs"

        raise NotImplementedError

    async def close(self) -> None:
        await self._client.aclose()
