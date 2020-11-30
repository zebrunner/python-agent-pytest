import pytest
from selenium.webdriver import Chrome, Firefox


def test_success() -> None:
    assert True


@pytest.mark.maintainer("admin")
def test_maintainer() -> None:
    assert True


@pytest.mark.skip(reason="Just skip this test")
def test_skip() -> None:
    assert True


@pytest.mark.xfail(reason="This test should fail!")
def test_xfail() -> None:
    assert False


def test_selenium() -> None:
    chrome = Chrome()
    firefox = Firefox()
    chrome.close()
    firefox.close()
    assert True
