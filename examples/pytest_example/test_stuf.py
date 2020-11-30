from typing import Callable

import pytest
from selenium.webdriver import Firefox


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


def test_selenium(send_screenshot: Callable) -> None:
    firefox = Firefox()
    firefox.get("https://www.google.com")
    firefox.save_screenshot("firefox.png")
    send_screenshot("firefox.png")
    firefox.close()
    assert True
