from typing import Callable

import pytest
from selenium.webdriver import Chrome


def test_success(send_artifact: Callable) -> None:
    send_artifact("geckodriver.log")
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
    firefox = Chrome()
    firefox.get("https://www.github.com")
    firefox.save_screenshot("firefox.png")
    send_screenshot("firefox.png")
    firefox.close()
    assert True
