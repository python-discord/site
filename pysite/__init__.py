# coding=utf-8
import logging
import sys
from logging import Logger, StreamHandler
from logging.handlers import SysLogHandler

from logmatic import JsonFormatter

from pysite.constants import DATADOG_ADDRESS, DATADOG_PORT, PAPERTRAIL_ADDRESS, PAPERTRAIL_PORT
from pysite.logs import NonPicklingSocketHandler

# region Logging
# Get the log level from environment

logging.TRACE = 5
logging.addLevelName(logging.TRACE, "TRACE")


def monkeypatch_trace(self, msg, *args, **kwargs):
    """
    Log 'msg % args' with severity 'TRACE'.

    To pass exception information, use the keyword argument exc_info with
    a true value, e.g.

    logger.trace("Houston, we have an %s", "interesting problem", exc_info=1)
    """
    if self.isEnabledFor(logging.TRACE):
        self._log(logging.TRACE, msg, args, **kwargs)


Logger.trace = monkeypatch_trace
log_level = logging.TRACE
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
