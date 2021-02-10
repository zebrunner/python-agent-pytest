from typing import Optional


class ZebrunnerContext:
    def __init__(self) -> None:
        self.test_run_id: Optional[int] = None
        self.test_id: Optional[int] = None

    @property
    def test_is_active(self) -> bool:
        return self.test_run_id is not None and self.test_id is not None

    @property
    def test_run_is_active(self) -> bool:
        return self.test_run_id is not None


zebrunner_context = ZebrunnerContext()
