import logging

from .plugin import connector_obj


class ZebrunnerRestHandler(logging.Handler):
    def __init__(self) -> None:
        logging.Handler.__init__(self, level=10)
        self.state = connector_obj.state

    def emit(self, record: logging.LogRecord) -> None:
        test_run = self.state.test_run
        test = self.state.test

        if test_run and test:
            test_run_id = test_run.json()["id"]
            test_id = test["id"]
            self.state.zc.push_log_record(test_run_id, test_id, record)
