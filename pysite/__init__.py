# coding=utf-8
import logging
import os
import sys
from logging import StreamHandler
from logging.handlers import SysLogHandler

from logmatic import JsonFormatter

from pysite.constants import DATADOG_ADDRESS, DATADOG_PORT, PAPERTRAIL_ADDRESS, PAPERTRAIL_PORT
from pysite.logs import NonPicklingSocketHandler

# region Logging
# Get the log level from environment

log_level = os.environ.get("LOG_LEVEL", "debug").upper()

if hasattr(logging, log_level):
    log_level = getattr(logging, log_level)
else:
    raise RuntimeError(f"LOG_LEVEL environment variable has invalid value: {log_level}")

logging_handlers = []

if PAPERTRAIL_ADDRESS:
    logging_handlers.append(SysLogHandler(address=(PAPERTRAIL_ADDRESS, PAPERTRAIL_PORT)))

if DATADOG_ADDRESS:
    datadog_handler = NonPicklingSocketHandler(host=DATADOG_ADDRESS, port=DATADOG_PORT)
    datadog_handler.formatter = JsonFormatter(datefmt="%b %d %H:%M:%S")

    logging_handlers.append(datadog_handler)

logging_handlers.append(StreamHandler(stream=sys.stderr))

logging.basicConfig(
    format="%(asctime)s pd.beardfist.com Site: | %(name)35s | %(levelname)8s | %(message)s",
    datefmt="%b %d %H:%M:%S",
    level=log_level,
    handlers=logging_handlers
)
# endregion
