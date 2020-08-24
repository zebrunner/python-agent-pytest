import pytest


class TestPluginIntegration:

    def test_passed(self):
        assert 1 == 1, 'is not as expected'

    def test_failed(self):
        assert 1 != 1, 'is not as expected'

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_skipped(self):
        assert 1 != 1, 'is not as expected'

    @pytest.mark.xfail(reason="xfail: blahblahblah")
    def test_xfailed(self):
        assert 1 != 1, 'is not as expected'
