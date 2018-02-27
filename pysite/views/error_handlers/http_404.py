# coding=utf-8
from werkzeug.exceptions import NotFound

from pysite.base_route import ErrorView
from flask import render_template

class Error404View(ErrorView):
    name = "error_404"
    error_code = 404

    def get(self, _error: NotFound):
        return render_template("errors/404.html", code="404"), 404
