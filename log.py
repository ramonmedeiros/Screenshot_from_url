import logging
import sys

from logging import INFO, DEBUG, CRITICAL, WARNING

logger = None
verbosity = logging.INFO


def getLogger():
    global logger
    if logger is None:
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger


def set_verbosity(verb):
    global verbosity
    verbosity = verb
    logger.setLevel(verbosity)
