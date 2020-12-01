import time
from logging import LogRecord, StreamHandler
from typing import List

from pytest_zebrunner.context import zebrunner_context
from pytest_zebrunner.zebrunner_api.client import ZebrunnerAPI
from pytest_zebrunner.zebrunner_api.models import LogRecordModel


class ZebrunnerHandler(StreamHandler):
    BATH_SIZE = 20
    logs: List[LogRecordModel] = []

    def __init__(self) -> None:
        super().__init__()
        self.api = ZebrunnerAPI()

    def emit(self, record: LogRecord) -> None:
        if len(self.logs) >= self.BATH_SIZE:
            self.push_logs()

        if zebrunner_context.test_id:
            self.logs.append(
                LogRecordModel(
                    test_id=str(zebrunner_context.test_id),
                    timestamp=str(round(time.time() * 1000)),
                    level=record.levelname,
                    message=record.message,
                )
            )

    def push_logs(self) -> None:
        logs = self.logs
        self.logs = []

        if zebrunner_context.test_run_id:
            self.api.send_logs(zebrunner_context.test_run_id, logs)
