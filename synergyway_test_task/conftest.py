# region				-----External Imports-----
import logging

# endregion


def pytest_configure(config):
    logging.getLogger("faker").setLevel(logging.WARNING)
