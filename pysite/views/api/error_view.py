# coding=utf-8
from flask import jsonify
from werkzeug.exceptions import HTTPException

from pysite.base_route import ErrorView


class APIErrorView(ErrorView):
    name = "api_error_all"
    error_code = range(400, 600)

    def return_error(self, error: HTTPException):
        """
        Return a basic JSON object representing the HTTP error, as well as propegating its status code
        """

        return jsonify({
            "error_code": -1,
            "error_message": error.description
        }), error.code

    get = return_error
    post = return_error
    put = return_error
    delete = return_error
    patch = return_error
    connect = return_error
    options = return_error
    trace = return_error
