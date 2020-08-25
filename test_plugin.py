import logging

import pytest


class TestPluginIntegration:

    LOGGER = logging.getLogger('ui')

    def test_passed(self):
        self.LOGGER.info('PASS')
        assert 1 == 1, 'is not as expected'

    def test_failed(self):
        self.LOGGER.info('FAIL')
        assert 1 != 1, 'is not as expected'

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_skipped(self):
        self.LOGGER.info('SKIP')
        assert 1 != 1, 'is not as expected'

    @pytest.mark.xfail(reason="xfail: blahblahblah")
    def test_xfailed(self):
        self.LOGGER.info('XFAIL')
        assert 1 != 1, 'is not as expected'
