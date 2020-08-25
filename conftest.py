import os

import urllib3
import logging
import logging.config

import yaml

from zebrunnerpy import connector_obj, PyTestZafiraListener

pytest_plugins = ['zebrunnerpy.plugin']
connector_obj.pytest_listener = PyTestZafiraListener(connector_obj.state)

path = os.getcwd()
config = yaml.load(open(os.path.join(path, 'logging.cfg'), 'r'))
logging.config.dictConfig(config)


def pytest_configure(config):
    """
    Attaches wrapped hooks as plugin
    """
    config.pluginmanager.register(connector_obj.pytest_listener)


def pytest_sessionstart(session):
    # basic settings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
