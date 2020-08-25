import logging

from .plugin import connector_obj


class ZebrunnerRestHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self, level=10)
        self.state = connector_obj.state

    def emit(self, record):
        test_run_id = self.state.test_run.json()["id"]
        test_id = self.state.test["id"]
        self.state.zc.push_log_record(test_run_id, test_id, record)
