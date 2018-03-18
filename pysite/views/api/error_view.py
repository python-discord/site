# coding=utf-8
from flask import jsonify
from werkzeug.exceptions import HTTPException

from pysite.base_route import ErrorView


class APIErrorView(ErrorView):
    name = "api_error_all"
    error_code = range(400, 600)

    def __init__(self):

        # Direct errors for all methods at self.return_error
        methods = [
            'get', 'post', 'put',
            'delete', 'patch', 'connect',
            'options', 'trace'
        ]

        for method in methods:
            setattr(self, method, self.return_error)

    def return_error(self, error: HTTPException):
        """
        Return a basic JSON object representing the HTTP error,
        as well as propagating its status code
        """

        message = str(error)
        code = 500

        if isinstance(error, HTTPException):
            message = error.description
            code = error.code

        return jsonify({
            "error_code": -1,
            "error_message": message
        }), code
