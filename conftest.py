import urllib3
import logging

logging.basicConfig()

from zebrunnerpy import connector_obj, PyTestZafiraListener

pytest_plugins = ['zebrunnerpy.plugin']
connector_obj.pytest_listener = PyTestZafiraListener(connector_obj.state)


def pytest_configure(config):
    """
    Attaches wrapped hooks as plugin
    """
    config.pluginmanager.register(connector_obj.pytest_listener)


def pytest_sessionstart(session):
    # basic settings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
