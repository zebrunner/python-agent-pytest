from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


def generate_uuid() -> str:
    return str(uuid4())


def generate_datetime_str() -> str:
    return datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()


class TestStatus(Enum):
    UNKNOWN = "UNKNOWN"
    IN_PROGRESS = "IN_PROGRESS"
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    ABORTED = "ABORTED"
    QUEUED = "QUEUED"


def to_camel_case(key: str) -> str:
    parts = key.split("_")
    for i, part in enumerate(parts[1:]):
        parts[i + 1] = part.capitalize()

    return "".join(parts)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel_case
        allow_population_by_field_name = True


class StartTestRunModel(CamelModel):
    name: str
    framework: str
    started_at: str = Field(default_factory=generate_datetime_str)
    uuid: str = Field(default_factory=generate_uuid)
    launch_context: Optional[dict] = None
    config: Optional[dict] = None


class StartTestModel(CamelModel):
    name: str
    class_name: str
    method_name: str
    uuid: str = Field(default_factory=generate_uuid)
    started_at: str = Field(default_factory=generate_datetime_str)
    maintainer: Optional[str] = None
    test_case: Optional[str] = None
    test_session_refs: Optional[list] = None


class FinishTestModel(CamelModel):
    result: str
    ended_at: str = Field(default_factory=generate_datetime_str)
    reason: Optional[str] = None
    labels: Optional[Dict[str, List[str]]] = None
    test_session_refs: Optional[list] = None


class LogRecordModel(BaseModel):
    test_id: str
    level: str
    timestamp: str
    message: str


if __name__ == "__main__":
    print()
