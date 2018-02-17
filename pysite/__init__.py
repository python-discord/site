# coding=utf-8
import logging
import os


# region Logging
# Get the log level from environment
log_level = os.environ.get("LOG_LEVEL", "info").lower()
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

if log_level == 'debug':
    log_level = logging.DEBUG
elif log_level == 'info':
    log_level = logging.INFO
elif log_level == 'error':
    log_level = logging.ERROR
elif log_level == 'critical':
    log_level = logging.CRITICAL
elif log_level == 'warning':
    log_level = logging.WARNING
else:
    raise RuntimeError("LOG_LEVEL environment variable has an invalid value.")

# This handler will ensure we log to stdout and stderr
ch = logging.StreamHandler()
ch.setLevel(log_level)
ch.setFormatter(formatter)

logger = logging.getLogger('site')
logger.setLevel(log_level)
logger.addHandler(ch)
# endregion
