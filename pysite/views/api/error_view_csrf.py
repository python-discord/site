# coding=utf-8
from flask import jsonify
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException

from pysite.base_route import ErrorView
from pysite.constants import ErrorCodes


class APIErrorViewCSRF(ErrorView):
    name = "error_csrf"
    error_code = CSRFError
    register_on_app = False

    def __init__(self):

        # Direct errors for all methods at self.return_error
        methods = [
            'get', 'post', 'put',
            'delete', 'patch', 'connect',
            'options', 'trace'
        ]

        for method in methods:
            setattr(self, method, self.return_error)

    def return_error(self, error: CSRFError):
        """
        Return a basic JSON object representing the HTTP error,
        as well as propagating its status code
        """

        return jsonify({
            "error_code": ErrorCodes.unauthorized,
            "error_message": "Bad CSRF token"
        }), error.code
