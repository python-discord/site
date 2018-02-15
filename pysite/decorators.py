# coding=utf-8
import os

from flask import request

from pysite.constants import ErrorCodes


def valid_api_key(f):
    """
    Decorator to check if X-API-Key is valid.

    Should only be applied to functions on APIView routes.
    """

    def has_valid_api_key(self, *args, **kwargs):
        if not request.headers.get("X-API-Key") == os.environ.get("API_KEY"):
            return self.error(ErrorCodes.invalid_api_key)
        return f(*args, **kwargs)

    return has_valid_api_key
