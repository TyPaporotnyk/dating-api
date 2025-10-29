import logging

from dating.config import LOG_LEVEL
from dating.enums import DatingEnum

LOG_FORMAT_DEBUG = "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"


class LogLevels(DatingEnum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"


def configure_logging():
    log_level = str(LOG_LEVEL).upper()
    log_levels = list(LogLevels)

    if log_level not in log_levels:
        log_level = LogLevels.error

    logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
