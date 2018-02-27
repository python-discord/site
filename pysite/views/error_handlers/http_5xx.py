# coding=utf-8
from werkzeug.exceptions import HTTPException

from pysite.base_route import ErrorView
from flask import render_template, request

class Error500View(ErrorView):
    name = "error_5xx"
    error_code = range(500, 600)

    def get(self, error: HTTPException):
        return render_template("errors/5XX.html", code=error.code, req=request), error.code
