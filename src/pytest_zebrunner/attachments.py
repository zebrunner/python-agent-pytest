import logging
from pathlib import Path
from typing import Union

from pytest_zebrunner.api.client import ZebrunnerAPI
from pytest_zebrunner.api.models import ArtifactReferenceModel, LabelModel
from pytest_zebrunner.context import zebrunner_context
from pytest_zebrunner.errors import AgentApiError, AgentError


def attach_test_screenshot(path: Union[str, Path]) -> None:
    """
    Send screenshot to zebrunner and attach it to test
    """
    if not zebrunner_context.test_is_active:
        raise AgentError("There is no active test to attach screenshot")

    try:
        api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
        api.send_screenshot(zebrunner_context.test_run_id, zebrunner_context.test_id, path)
    except AgentApiError as e:
        logging.error("Failed to attach test screenshot", exc_info=e)


def attach_test_artifact(path: Union[str, Path]) -> None:
    """
    Send artifact to zebrunner and attach it to test. Artifact is any file from disk
    """
    if not zebrunner_context.test_is_active:
        raise AgentError("There is no active test to attach artifact")

    try:
        api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
        api.send_artifact(path, zebrunner_context.test_run_id, zebrunner_context.test_id)
    except AgentApiError as e:
        logging.error("Failed to attach test artifact", exc_info=e)


def attach_test_run_artifact(path: Union[str, Path]) -> None:
    """
    Send artifact to zebrunner and attach it to test run. Artifact is any file from disk
    """
    if not zebrunner_context.test_run_is_active:
        raise AgentError("There is no active test run to attach artifact")

    try:
        api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
        api.send_artifact(path, zebrunner_context.test_run_id)
    except AgentApiError as e:
        logging.error("Failed to attach test run artifact", exc_info=e)


def attach_test_artifact_reference(name: str, ref: str) -> None:
    """
    Send artifact reference to zebrunner and attach it to test. Artifact reference is a URL
    """
    if not zebrunner_context.test_is_active:
        raise AgentError("There is no active test to attach artifact reference")

    try:
        api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
        api.send_artifact_references(
            [ArtifactReferenceModel(name=name, value=ref)], zebrunner_context.test_run_id, zebrunner_context.test_id
        )
    except AgentApiError as e:
        logging.error("Failed to attach test artifact reference", exc_info=e)


def attach_test_run_artifact_reference(name: str, ref: str) -> None:
    """
    Send artifact reference to zebrunner and attach it to test run. Artifact reference is a URL
    """
    if not zebrunner_context.test_run_is_active:
        raise AgentError("There is no active test run to attach artifact reference")

    try:
        api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
        api.send_artifact_references([ArtifactReferenceModel(name=name, value=ref)], zebrunner_context.test_run_id)
    except AgentApiError as e:
        logging.error("Failed to attach test run artifact reference", exc_info=e)


def attach_test_label(name: str, value: str) -> None:
    """
    Attach label to test in zebrunner
    """
    if not zebrunner_context.test_is_active:
        raise AgentError("There is no active test to attach label")

    try:
        api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
        api.send_labels([LabelModel(key=name, value=value)], zebrunner_context.test_run_id, zebrunner_context.test_id)
    except AgentApiError as e:
        logging.error("Failed to attach label to test", exc_info=e)


def attach_test_run_label(name: str, value: str) -> None:
    """
    Attach label to test run in zebrunner
    """
    if not zebrunner_context.test_run_is_active:
        raise AgentError("There is no active test run to attach label")

    try:
        api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
        api.send_labels([LabelModel(key=name, value=value)], zebrunner_context.test_run_id)
    except AgentApiError as e:
        logging.error("Failed to attach label to test run", exc_info=e)
