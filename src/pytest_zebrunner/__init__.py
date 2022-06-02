from pytest_zebrunner.attachments import (
    attach_test_artifact,
    attach_test_artifact_reference,
    attach_test_label,
    attach_test_run_artifact,
    attach_test_run_artifact_reference,
    attach_test_run_label,
    attach_test_screenshot,
)

from .current_test import CurrentTest  # noqa: F401
from .current_test_run import CurrentTestRun  # noqa: F401

__version__ = "1.5.6"
__all__ = [
    "attach_test_artifact_reference",
    "attach_test_run_artifact_reference",
    "attach_test_label",
    "attach_test_run_label",
    "attach_test_artifact",
    "attach_test_run_artifact",
    "attach_test_screenshot",
]
