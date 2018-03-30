# coding=utf-8
import os
from functools import wraps
from json import JSONDecodeError

from flask import request, redirect, url_for
from schema import Schema, SchemaError
from werkzeug.exceptions import Forbidden

from pysite.base_route import APIView, BaseView
from pysite.constants import ErrorCodes, ValidationTypes


def require_roles(*roles: int):
    def inner_decorator(f):

        @wraps(f)
        def inner(self: BaseView, *args, **kwargs):
            data = self.user_data

            if data:
                for role in roles:
                    if role in data["roles"]:
                        return f(self, *args, **kwargs)

                raise Forbidden()
            return redirect(url_for("discord.login"))
        return inner

    return inner_decorator


def api_key(f):
    """
    Decorator to check if X-API-Key is valid.

    Should only be applied to functions on APIView routes.
    """

    @wraps(f)
    def inner(self: APIView, *args, **kwargs):
        if not request.headers.get("X-API-Key") == os.environ.get("BOT_API_KEY"):
            return self.error(ErrorCodes.invalid_api_key)
        return f(self, *args, **kwargs)

    return inner


def api_params(schema: Schema, validation_type: ValidationTypes = ValidationTypes.json):
    """
    Validate parameters of data passed to the decorated view.

    Should only be applied to functions on APIView routes.

    This will pass the validated data in as the first parameter to the decorated function.
    This data will always be a list, and view functions are expected to be able to handle that
    in the case of multiple sets of data being provided by the api.
    """
    def inner_decorator(f):

        @wraps(f)
        def inner(self: BaseView, *args, **kwargs):
            if validation_type == ValidationTypes.json:
                try:
                    if not request.is_json:
                        return self.error(ErrorCodes.bad_data_format)

                    data = request.get_json()

                    if not isinstance(data, list):
                        data = [data]

                except JSONDecodeError:
                    return self.error(ErrorCodes.bad_data_format)  # pragma: no cover

            elif validation_type == ValidationTypes.params:
                # I really don't like this section here, but I can't think of a better way to do it
                multi = request.args  # This is a MultiDict, which should be flattened to a list of dicts

                # We'll assume that there's always an equal number of values for each param
                # Anything else doesn't really make sense anyway
                data = []
                longest = None

                for _key, items in multi.lists():
                    # Make sure every key has the same number of values
                    if longest is None:
                        # First iteration, store it
                        longest = len(items)

                    elif len(items) != longest:  # pragma: no cover
                        # At least one key has a different number of values
                        return self.error(ErrorCodes.bad_data_format)  # pragma: no cover

                if longest is not None:
                    for i in range(longest):  # Now we know all keys have the same number of values...
                        obj = {}  # New dict to store this set of values

                        for key, items in multi.lists():
                            obj[key] = items[i]  # Store the item at that specific index

                        data.append(obj)

            else:
                raise ValueError(f"Unknown validation type: {validation_type}")  # pragma: no cover

            try:
                schema.validate(data)
            except SchemaError:
                return self.error(ErrorCodes.incorrect_parameters)

            return f(self, data, *args, **kwargs)
        return inner
    return inner_decorator
