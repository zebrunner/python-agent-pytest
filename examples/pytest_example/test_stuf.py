import pytest


def test_success() -> None:
    assert True


@pytest.mark.maintainer("admin")
def test_maintainer() -> None:
    assert True


@pytest.mark.skip
def test_skip() -> None:
    assert True


@pytest.mark.xfail
def test_xfail() -> None:
    assert False
