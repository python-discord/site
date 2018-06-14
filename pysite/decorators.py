from functools import wraps
from json import JSONDecodeError

from flask import request
from schema import Schema, SchemaError
from werkzeug.exceptions import BadRequest, Forbidden

from pysite.base_route import APIView, RouteView
from pysite.constants import BOT_API_KEY, CSRF, DEBUG_MODE, ErrorCodes, ValidationTypes


def csrf(f):
    """
    Apply CSRF protection to a specific view function.
    """

    @wraps(f)
    def inner_decorator(*args, **kwargs):
        CSRF.protect()

        return f(*args, **kwargs)

    return inner_decorator


def require_roles(*roles: int):
    def inner_decorator(f):

        @wraps(f)
        def inner(self: RouteView, *args, **kwargs):
            data = self.user_data

            if DEBUG_MODE:
                return f(self, *args, **kwargs)
            elif data:
                for role in roles:
                    if role in data.get("roles", []):
                        return f(self, *args, **kwargs)

                if isinstance(self, APIView):
                    return self.error(ErrorCodes.unauthorized)

                raise Forbidden()
            return self.redirect_login(**kwargs)

        return inner

    return inner_decorator


def api_key(f):
    """
    Decorator to check if X-API-Key is valid.

    Should only be applied to functions on APIView routes.
    """

    @wraps(f)
    def inner_decorator(self: APIView, *args, **kwargs):
        if not request.headers.get("X-API-Key") == BOT_API_KEY:
            return self.error(ErrorCodes.invalid_api_key)
        return f(self, *args, **kwargs)

    return inner_decorator


def api_params(
        schema: Schema,
        validation_type: ValidationTypes = ValidationTypes.json,
        allow_duplicate_params: bool = False):
    """
    Validate parameters of data passed to the decorated view.

    Should only be applied to functions on APIView routes.

    This will pass the validated data in as the first parameter to the decorated function.
    This data will always be a list, and view functions are expected to be able to handle that
    in the case of multiple sets of data being provided by the api.

    If `allow_duplicate_params` is set to False (only effects dictionary schemata
    and parameter validation), then the view will return a 400 Bad Request
    response if the client submits multiple parameters with the same name.
    """

    def inner_decorator(f):

        @wraps(f)
        def inner(self: APIView, *args, **kwargs):
            if validation_type == ValidationTypes.json:
                try:
                    if not request.is_json:
                        return self.error(ErrorCodes.bad_data_format)

                    data = request.get_json()

                    if not isinstance(data, list) and isinstance(schema._schema, list):
                        data = [data]

                except JSONDecodeError:
                    return self.error(ErrorCodes.bad_data_format)  # pragma: no cover

            elif validation_type == ValidationTypes.params and isinstance(schema._schema, list):
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

            elif validation_type == ValidationTypes.params and isinstance(schema._schema, dict):
                if not allow_duplicate_params:
                    for _arg, value in request.args.to_dict(flat=False).items():
                        if len(value) > 1:
                            raise BadRequest("This view does not allow duplicate query arguments")
                data = request.args.to_dict()

            else:
                raise ValueError(f"Unknown validation type: {validation_type}")  # pragma: no cover

            try:
                schema.validate(data)
            except SchemaError:
                return self.error(ErrorCodes.incorrect_parameters)

            return f(self, data, *args, **kwargs)

        return inner

    return inner_decorator
