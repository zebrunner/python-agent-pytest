from pathlib import Path
from typing import Union

from pytest_zebrunner.api.client import ZebrunnerAPI
from pytest_zebrunner.api.models import ArtifactReferenceModel, LabelModel
from pytest_zebrunner.context import zebrunner_context


def attach_test_screenshot(path: Union[str, Path]) -> None:
    """
    Attach a screenshot to the test in scope of Zebrunner Reporting in order to track it.

    Args:
        path (Union[str, Path]): Path to identify image location in directory structure.
    """
    api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
    if zebrunner_context.test_is_active:
        api.send_screenshot(zebrunner_context.test_run_id, zebrunner_context.test_id, path)


def attach_test_artifact(path: Union[str, Path]) -> None:
    """
    Attach an artifact to the test in scope of Zebrunner Reporting in order to track it.
    The display name provided must contain the file extension that reflects file's content.

    Args:
        path (Union[str, Path]): Path to identify artifact location in directory structure.
    """
    api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
    if zebrunner_context.test_is_active:
        api.send_artifact(path, zebrunner_context.test_run_id, zebrunner_context.test_id)


def attach_test_run_artifact(path: Union[str, Path]) -> None:
    """
    Attach an artifact to the test_run in scope of Zebrunner Reporting in order to track it.
    The display name provided must contain the file extension that reflects file's content.

    Args:
        path (Union[str, Path]): Path to identify artifact location in directory structure.
    """
    api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
    if zebrunner_context.test_run_is_active:
        api.send_artifact(path, zebrunner_context.test_run_id)


def attach_test_artifact_reference(name: str, ref: str) -> None:
    """
    Attach an artifact reference to the test in scope of Zebrunner Reporting in order to track it.

    Args:
        name (str): Arbitrary name to identify the reference.
        ref (str): Reference to the artifact.
    """
    api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
    if zebrunner_context.test_is_active:
        api.send_artifact_references(
            [ArtifactReferenceModel(name=name, value=ref)], zebrunner_context.test_run_id, zebrunner_context.test_id
        )


def attach_test_run_artifact_reference(name: str, ref: str) -> None:
    """
    Attach an artifact reference to the test_run in scope of Zebrunner Reporting in order to track it.

    Args:
        name (str): Arbitrary name to identify the reference
        ref (str): Reference to the artifact.
    """
    api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
    if zebrunner_context.test_run_is_active:
        api.send_artifact_references([ArtifactReferenceModel(name=name, value=ref)], zebrunner_context.test_run_id)


def attach_test_label(name: str, value: str) -> None:
    """
    Attach meta data to the test as key-value pair, in scope of Zebrunner Reporting in order to track it.

    Args:
        name (str): Key of key-value pair.
        value (str): Value of key-value pair.
    """
    api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
    if zebrunner_context.test_is_active:
        api.send_labels([LabelModel(key=name, value=value)], zebrunner_context.test_run_id, zebrunner_context.test_id)


def attach_test_run_label(name: str, value: str) -> None:
    """
    Attach meta data to the test_run as key-value pair, in scope of Zebrunner Reporting in order to track it.

    Args:
        name (str): Key of key-value pair.
        value (str): Value of key-value pair.
    """
    api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
    if zebrunner_context.test_run_is_active:
        api.send_labels([LabelModel(key=name, value=value)], zebrunner_context.test_run_id)
