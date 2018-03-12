# coding=utf-8
import logging
import os
from logging import StreamHandler
from logging.handlers import SysLogHandler
import sys

from pysite.constants import PAPERTRAIL_ADDRESS, PAPERTRAIL_PORT

# region Logging
# Get the log level from environment
log_level = os.environ.get("LOG_LEVEL", "info").upper()

if hasattr(logging, log_level):
    log_level = getattr(logging, log_level)
else:
    raise RuntimeError("LOG_LEVEL environment variable has an invalid value.")

logging_handlers = []

if PAPERTRAIL_ADDRESS:
    logging_handlers.append(SysLogHandler(address=(PAPERTRAIL_ADDRESS, PAPERTRAIL_PORT)))

logging_handlers.append(StreamHandler(stream=sys.stderr))

logging.basicConfig(
    format="%(asctime)s pd.beardfist.com Site: | %(name)30s | %(levelname)8s | %(message)s",
    datefmt="%b %d %H:%M:%S",
    level=log_level,
    handlers=logging_handlers
)
# endregion
