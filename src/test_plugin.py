import pytest


def test_passed() -> None:
    assert True


@pytest.mark.maintainer("admin")
def test_maintainer() -> None:
    assert True


@pytest.mark.skip
def test_skipped() -> None:
    assert True


def test_failed() -> None:
    assert False


def test_error() -> None:
    raise ValueError()
