"""
This file provides convenient access to the python logging functionality. It
makes sure that logging calls are redirected to standard out and to different
log files according to severity.

More information about formatting can be found at
https://docs.python.org/3/library/logging.html#logging.LogRecord
"""

import logging
import sys
from logging import Logger

from colorlog import ColoredFormatter


def init_logger(name: str) -> Logger:
    """
    Initializes two file-loggers and a console, satisfying the aidkitlite log
    format.

    :param name: Name of logger.
    :return: Logger satisfying the aidkitlite log format.
    """
    console_handler = create_console_handler()

    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    logger.handlers = []
    logger.addHandler(console_handler)

    return logger


def create_console_handler() -> logging.StreamHandler:
    """
    Log handler for displaying logs in the console.

    :return: colored log handler
    """
    color_formatter = create_colored_formatter()
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(color_formatter)
    return console_handler


def create_colored_formatter() -> ColoredFormatter:
    """
    Facilitate colorlog to distinguish the loglevels visually.

    :return: good colored formatter
    """
    color_codes = {
        'NOTSET': 'white',
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red',
    }
    color_formatter = ColoredFormatter(
        fmt=(
            '%(log_color)s%(asctime)s: %(levelname)-8s: %(name)-20s: line %(lineno)-4d: %(message)s'
        ),
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors=color_codes,
    )
    return color_formatter
