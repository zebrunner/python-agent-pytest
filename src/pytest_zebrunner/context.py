from datetime import datetime
from typing import List, Optional, Tuple

from pydantic.error_wrappers import ValidationError

from pytest_zebrunner.settings import load_settings


class TestRun:
    def __init__(self, name: str = None, environment: str = None, build: str = None) -> None:
        self.zebrunner_id: Optional[int] = None
        self.name = name or f"Unnamed {datetime.utcnow()}"
        self.environment = environment
        self.build = build


class Test:
    def __init__(self, name: str, file: str, maintainers: List[str], labels: List[Tuple[str, str]]) -> None:
        self.zebrunner_id: Optional[int] = None
        self.name = name
        self.file = file
        self.maintainers = maintainers
        self.labels = labels
        self.is_reverted = False


class ZebrunnerContext:
    def __init__(self) -> None:
        self.test_run: Optional[TestRun] = None
        self.test: Optional[Test] = None
        try:
            self.settings = load_settings()
        except ValidationError:
            self.settings = None  # type: ignore

    @property
    def is_configured(self) -> bool:
        return self.settings is not None

    @property
    def test_is_active(self) -> bool:
        return self.is_configured and self.test_run_is_active and self.test_id is not None

    @property
    def test_run_is_active(self) -> bool:
        return self.is_configured and self.test_run_id is not None

    @property
    def test_id(self) -> int:
        return getattr(self.test, "zebrunner_id", None)

    @property
    def test_run_id(self) -> int:
        return getattr(self.test_run, "zebrunner_id", None)


zebrunner_context = ZebrunnerContext()
