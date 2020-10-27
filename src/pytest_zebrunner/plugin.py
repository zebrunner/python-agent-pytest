from .zafira_state import ZafiraState


class PytestZafiraConnector:
    """
    An instance of Zafira connector with generic Zafira state,
    Can be instantiated as pytest connector,
    or behave connector according to a running context
    """
    def __init__(self):
        self.state = ZafiraState()


connector_obj = PytestZafiraConnector()
