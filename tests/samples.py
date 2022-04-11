import pytest
from selenium.webdriver import Remote

from pytest_zebrunner import (
    attach_test_artifact,
    attach_test_artifact_reference,
    attach_test_label,
    attach_test_run_artifact,
    attach_test_run_label,
    attach_test_screenshot,
)


def test_success() -> None:
    assert True


@pytest.mark.maintainer("aplatonov")
def test_maintainer() -> None:
    assert True


@pytest.mark.skip(reason="Just skip this test")
def test_skip() -> None:
    assert True


@pytest.mark.xfail(reason="This test should fail!")
def test_xfail() -> None:
    assert False


def test_fail() -> None:
    raise ValueError("This test fail by exception")


def test_selenium_firefox() -> None:
    firefox = Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities={"browserName": "firefox"})
    firefox.quit()
    assert True


def test_selenium_chrome() -> None:
    chrome = Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities={"browserName": "chrome"})
    chrome.quit()
    assert True


def test_selenium_both() -> None:
    chrome = Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities={"browserName": "chrome"})
    firefox = Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities={"browserName": "firefox"})
    chrome.quit()
    firefox.quit()
    assert True


def test_send_screenshot() -> None:
    chrome = Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities={"browserName": "chrome"})
    chrome.get("https://www.google.com")
    chrome.save_screenshot("google.png")
    attach_test_screenshot("google.png")
    chrome.quit()
    assert True


def test_send_artifact() -> None:
    firefox = Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities={"browserName": "firefox"})
    firefox.get("https://www.google.com")
    firefox.quit()
    attach_test_artifact("geckodriver.log")
    attach_test_run_artifact("geckodriver.log")
    attach_test_artifact_reference("name", "reference")
    assert True


@pytest.mark.label("header", "label")
@pytest.mark.label("header", "label2")
def test_labels() -> None:
    attach_test_label("body", "label")
    attach_test_run_label("body", "test_run_label")
    assert True


@pytest.mark.artifact("pyproject.toml")
def test_artifact() -> None:
    assert True


@pytest.mark.artifact("pyproject.toml")
@pytest.mark.artifact("mypy.ini")
def test_multiple_artifact() -> None:
    assert True


@pytest.mark.artifact_reference("github", "https://www.github.com")
@pytest.mark.artifact_reference("google", "https://google.com")
def test_artifact_reference() -> None:
    assert True


class TestGroup:
    def test_class_method1(self) -> None:
        assert True

    def test_class_method2(self) -> None:
        assert True
