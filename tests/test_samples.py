import pytest
from selenium.webdriver import Chrome, Firefox, Remote

from pytest_zebrunner import attachments


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


def test_selenium_firefox() -> None:
    firefox = Remote(
        command_executor="http://localhost:4444/wd/hub/", 
        desired_capabilities={"browserName": "firefox"}
    )
    firefox.quit()
    assert True


def test_selenium_chrome() -> None:
    chrome = Remote(
        command_executor="http://localhost:4444/wd/hub/", 
        desired_capabilities={"browserName": "chrome"}
    )
    chrome.quit()
    assert True


def test_selenium_both() -> None:
    chrome = Remote(
        command_executor="http://localhost:4444/wd/hub/", 
        desired_capabilities={"browserName": "chrome"}
    )
    firefox = Remote(
        command_executor="http://localhost:4444/wd/hub/", 
        desired_capabilities={"browserName": "firefox"}
    )
    chrome.quit()
    firefox.quit()
    assert True


def test_send_screenshot() -> None:
    chrome = Remote(
        command_executor="http://localhost:4444/wd/hub/", 
        desired_capabilities={"browserName": "chrome"}
    )
    chrome.get("https://www.google.com")
    chrome.save_screenshot("google.png")
    attachments.attach_test_screenshot("google.png")
    chrome.quit()
    assert True


def test_send_artifact() -> None:
    firefox = Remote(
        command_executor="http://localhost:4444/wd/hub/", 
        desired_capabilities={"browserName": "firefox"}
    )
    firefox.get("https://www.google.com")
    firefox.quit()
    attachments.attach_test_artifact("geckodriver.log")
    attachments.attach_test_run_artifact("geckodriver.log")
    attachments.attach_test_artifact_reference("name", "reference")
    assert True


@pytest.mark.label("header", "label")
@pytest.mark.label("header", "label2")
def test_labels() -> None:
    attachments.attach_test_label("body", "label")
    attachments.attach_test_run_label("body", "test_run_label")
    assert True
