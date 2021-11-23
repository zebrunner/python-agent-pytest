from pytest_zebrunner.attachments import (
    attach_test_artifact,
    attach_test_artifact_reference,
    attach_test_label,
    attach_test_run_artifact,
    attach_test_run_artifact_reference,
    attach_test_run_label,
    attach_test_screenshot,
)

__version__ = "1.4.0"
__all__ = [
    "attach_test_artifact_reference",
    "attach_test_run_artifact_reference",
    "attach_test_label",
    "attach_test_run_label",
    "attach_test_artifact",
    "attach_test_run_artifact",
    "attach_test_screenshot",
]
