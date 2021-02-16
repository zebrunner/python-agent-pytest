from pathlib import Path
from typing import Union

from pytest_zebrunner.api.client import ZebrunnerAPI
from pytest_zebrunner.api.models import ArtifactReferenceModel, LabelModel
from pytest_zebrunner.context import zebrunner_context

api = ZebrunnerAPI()


def attach_screenshot(path: Union[str, Path]) -> None:
    if zebrunner_context.test_is_active:
        api.send_screenshot(zebrunner_context.test_run_id, zebrunner_context.test_id, path)


def attach_test_artifact(path: Union[str, Path]) -> None:
    if zebrunner_context.test_is_active:
        api.send_artifact(path, zebrunner_context.test_run_id, zebrunner_context.test_id)


def attach_test_run_artifact(path: Union[str, Path]) -> None:
    if zebrunner_context.test_run_is_active:
        api.send_artifact(path, zebrunner_context.test_run_id)


def attach_test_artifact_reference(name: str, ref: str) -> None:
    if zebrunner_context.test_is_active:
        api.send_artifact_references(
            [ArtifactReferenceModel(name=name, value=ref)], zebrunner_context.test_run_id, zebrunner_context.test_id
        )


def attach_test_run_artifact_reference(name: str, ref: str) -> None:
    if zebrunner_context.test_run_is_active:
        api.send_artifact_references([ArtifactReferenceModel(name=name, value=ref)], zebrunner_context.test_run_id)


def attach_test_label(name: str, value: str) -> None:
    if zebrunner_context.test_is_active:
        api.send_labels([LabelModel(key=name, value=value)], zebrunner_context.test_run_id, zebrunner_context.test_id)


def attach_test_run_label(name: str, value: str) -> None:
    if zebrunner_context.test_run_is_active:
        api.send_labels([LabelModel(key=name, value=value)], zebrunner_context.test_run_id)
