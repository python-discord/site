import logging
import os


class Logs:
    def __init__(self, app):
        loglevel = os.environ.get("LOG_LEVEL", "info")
        loglevel = loglevel.lower()
        if 'debug' in loglevel:
            loglevel = logging.DEBUG
        if 'info' in loglevel:
            loglevel = logging.INFO

        self.log = logging.getLogger('werkzeug')
        self.log.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

        ch.setFormatter(formatter)
        self.log.addHandler(ch)
        self.log.debug('info message')

    def debug(self, message):
        self.log.debug(message)

    def info(self, message):
        self.log.info(message)
