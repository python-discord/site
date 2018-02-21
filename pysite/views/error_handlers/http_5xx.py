# coding=utf-8
from werkzeug.exceptions import HTTPException

from pysite.base_route import ErrorView


class Error404View(ErrorView):
    name = "error_5xx"
    error_code = range(500, 600)

    def get(self, error: HTTPException):
        return "Internal server error. Please try again later!", error.code
