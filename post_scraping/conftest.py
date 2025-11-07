# region				-----External Imports-----
import logging
from tests.factories.user import *

# endregion


def pytest_configure(config):
    logging.getLogger("faker").setLevel(logging.WARNING)
