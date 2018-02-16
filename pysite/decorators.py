# coding=utf-8
import os
from functools import wraps
from json import JSONDecodeError

from flask import request

from schema import Schema, SchemaError

from pysite.constants import ErrorCodes, ValidationTypes


def api_key(f):
    """
    Decorator to check if X-API-Key is valid.

    Should only be applied to functions on APIView routes.
    """

    @wraps(f)
    def inner(self, *args, **kwargs):
        if not request.headers.get("X-API-Key") == os.environ.get("API_KEY"):
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
        def inner(self, *args, **kwargs):
            if validation_type == ValidationTypes.json:
                try:
                    if not request.is_json:
                        return self.error(ErrorCodes.bad_data_format)

                    data = list(request.get_json())
                except JSONDecodeError:
                    return self.error(ErrorCodes.bad_data_format)

            elif validation_type == ValidationTypes.params:
                # I really don't like this section here, but I can't think of a better way to do it
                multi = request.args  # This is a MultiDict, which should be flattened to a list of dicts

                # We'll assume that there's always an equal number of values for each param
                # Anything else doesn't really make sense anyway
                data = []
                longest = None

                for key, items in multi.lists():
                    # Make sure every key has the same number of values
                    if longest is None:
                        # First iteration, store it
                        longest = len(items)

                    elif len(items) != longest:
                        # At least one key has a different number of values
                        return self.error(ErrorCodes.bad_data_format)

                for i in range(longest):  # Now we know all keys have the same number of values...
                    obj = {}  # New dict to store this set of values

                    for key, items in multi.lists():
                        obj[key] = items[i]  # Store the item at that specific index

                    data.append(obj)

            else:
                raise ValueError(f"Unknown validation type: {validation_type}")

            try:
                schema.validate(data)
            except SchemaError:
                return self.error(ErrorCodes.incorrect_parameters)

            return f(self, data, *args, **kwargs)
        return inner
    return inner_decorator
