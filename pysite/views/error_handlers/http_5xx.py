# coding=utf-8
from flask import render_template, request
from werkzeug.exceptions import HTTPException

from pysite.base_route import ErrorView
from pysite.constants import ERROR_DESCRIPTIONS


class Error500View(ErrorView):
    name = "error_5xx"
    error_code = range(500, 600)

    def get(self, error: HTTPException):
        error_desc = ERROR_DESCRIPTIONS.get(error.code, "We're not really sure what happened there, please try again.")

        return render_template("errors/error.html", code=error.code, req=request, error_title=error_desc,
                               error_message="An error occurred while "
                                             "processing this "
                                             "request, please try "
                                             "again later. "
                                             "If you believe we have made a mistake, "
                                             "please "
                                             " <a href='https://github.com"
                                             "/discord-python/site/issues'>file an issue on our GitHub"
                                             "</a>."), error.code
