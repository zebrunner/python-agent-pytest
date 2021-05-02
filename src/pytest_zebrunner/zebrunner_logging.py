import time
from datetime import datetime, timedelta
from logging import LogRecord, StreamHandler
from typing import List

from pytest_zebrunner.api.client import ZebrunnerAPI
from pytest_zebrunner.api.models import LogRecordModel
from pytest_zebrunner.context import zebrunner_context


class ZebrunnerHandler(StreamHandler):
    logs: List[LogRecordModel] = []

    def __init__(self) -> None:
        super().__init__()
        self.api = ZebrunnerAPI()
        self.last_push = datetime.utcnow()

    def emit(self, record: LogRecord) -> None:
        if datetime.utcnow() - self.last_push >= timedelta(seconds=1):
            self.push_logs()

        if zebrunner_context.test_is_active:
            self.logs.append(
                LogRecordModel(
                    test_id=str(zebrunner_context.test_id),
                    timestamp=str(round(time.time() * 1000)),
                    level=record.levelname,
                    message=record.msg,
                )
            )

    def push_logs(self) -> None:
        self.last_push = datetime.utcnow()
        logs = self.logs
        self.logs = []

        if zebrunner_context.test_run_id:
            self.api.send_logs(zebrunner_context.test_run_id, logs)
