# region				-----External Imports-----
from __future__ import absolute_import, unicode_literals
from celery import signals
from celery import Celery
import os
import sys
import logging

# endregion

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

app = Celery("website")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.broker_transport_options = {
    "priority_steps": list(range(10)),
    "queue_order_strategy": "priority",
}


@signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s, %(thread)d  %(levelname)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
            "celery": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": "celery.log",
                "formatter": "default",
            },
            "default": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "loggers": {
            "celery": {
                "handlers": ["celery", "console"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "root": {"handlers": ["default"], "level": "DEBUG"},
    }

    logging.config.dictConfig(config)
