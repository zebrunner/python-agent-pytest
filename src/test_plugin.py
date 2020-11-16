from time import sleep

import pytest


def test_passed() -> None:
    sleep(1)
    assert True


@pytest.mark.maintainer("admin")
def test_maintainer() -> None:
    sleep(1)
    assert True


@pytest.mark.skip
def test_skipped() -> None:
    sleep(1)
    assert True


def test_failed() -> None:
    sleep(1)
    assert False


def test_error() -> None:
    sleep(1)
    raise ValueError()
