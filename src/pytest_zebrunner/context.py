from typing import Optional


class ZebrunnerContext:
    def __init__(self) -> None:
        self.test_run_id: Optional[int] = None
        self.test_id: Optional[int] = None


zebrunner_context = ZebrunnerContext()
