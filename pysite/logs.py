# coding=utf-8
from logging.handlers import SocketHandler


class NonPicklingSocketHandler(SocketHandler):
    def emit(self, record):
        try:
            s = self.formatter.format(record).encode() + b"\n"
            self.send(s)
        except Exception:
            self.handleError(record)
