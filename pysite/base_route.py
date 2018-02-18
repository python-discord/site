# coding=utf-8
import os
import random
import string

from flask import Blueprint, jsonify, render_template
from flask.views import MethodView

from pysite.constants import ErrorCodes


class BaseView(MethodView):
    """
    Base view class with functions and attributes that should be common to all view classes.

    This class should be subclassed, and is not intended to be used directly.
    """

    name = None  # type: str

    def render(self, *template_names, **context):
        context["current_page"] = self.name
        context["view"] = self

        return render_template(template_names, **context)


class RouteView(BaseView):
    """
    Standard route-based page view. For a standard page, this is what you want.

    This class is intended to be subclassed - use it as a base class for your own views, and set the class-level
    attributes as appropriate. For example:

    >>> class MyView(RouteView):
    ...     name = "my_view"  # Flask internal name for this route
    ...     path = "/my_view"  # Actual URL path to reach this route
    ...
    ...     def get(self):  # Name your function after the relevant HTTP method
    ...         return self.render("index.html")

    For more complicated routing, see http://exploreflask.com/en/latest/views.html#built-in-converters
    """

    path = None  # type: str

    @classmethod
    def setup(cls: "RouteView", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        """
        Set up the view by adding it to the blueprint passed in - this will also deal with multiple inheritance by
        calling `super().setup()` as appropriate.

        This is for a standard route view. Nothing special here.

        :param manager: Instance of the current RouteManager
        :param blueprint: Current Flask blueprint to register this route to
        """

        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)

        if not cls.path or not cls.name:
            raise RuntimeError("Route views must have both `path` and `name` defined")

        blueprint.add_url_rule(cls.path, view_func=cls.as_view(cls.name))


class APIView(RouteView):
    """
    API route view, with extra methods to help you add routes to the JSON API with ease.

    This class is intended to be subclassed - use it as a base class for your own views, and set the class-level
    attributes as appropriate. For example:

    >>> class MyView(APIView):
    ...     name = "my_view"  # Flask internal name for this route
    ...     path = "/my_view"  # Actual URL path to reach this route
    ...
    ...     def get(self):  # Name your function after the relevant HTTP method
    ...         return self.error(ErrorCodes.unknown_route)
    """

    def validate_key(self, api_key: str):
        """ Placeholder! """
        return api_key == os.environ.get("API_KEY")

    def generate_api_key(self):
        """ Generate a random string of n characters. """
        pool = random.choices(string.ascii_letters + string.digits, k=32)
        return "".join(pool)

    def error(self, error_code: ErrorCodes):

        data = {
            "error_code": error_code.value,
            "error_message": "Unknown error"
        }

        http_code = 200

        if error_code is ErrorCodes.unknown_route:
            data["error_message"] = "Unknown API route"
            http_code = 404
        elif error_code is ErrorCodes.unauthorized:
            data["error_message"] = "Unauthorized"
            http_code = 401
        elif error_code is ErrorCodes.invalid_api_key:
            data["error_message"] = "Invalid API-key"
            http_code = 401
        elif error_code is ErrorCodes.bad_data_format:
            data["error_message"] = "Input data in incorrect format"
            http_code = 400
        elif error_code is ErrorCodes.incorrect_parameters:
            data["error_message"] = "Incorrect parameters provided"
            http_code = 400

        response = jsonify(data)
        response.status_code = http_code
        return response


class ErrorView(BaseView):
    """
    Error view, shown for a specific HTTP status code, as defined in the class attributes.

    This class is intended to be subclassed - use it as a base class for your own views, and set the class-level
    attributes as appropriate. For example:

    >>> class MyView(ErrorView):
    ...     name = "my_view"  # Flask internal name for this route
    ...     path = "/my_view"  # Actual URL path to reach this route
    ...     error_code = 404
    ...
    ...     def get(self):  # Name your function after the relevant HTTP method
    ...         return "Replace me with a template, 404 not found", 404
    """

    error_code = None  # type: int

    @classmethod
    def setup(cls: "ErrorView", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        """
        Set up the view by registering it as the error handler for the HTTP status code specified in the class
        attributes - this will also deal with multiple inheritance by calling `super().setup()` as appropriate.

        :param manager: Instance of the current RouteManager
        :param blueprint: Current Flask blueprint to register the error handler for
        """

        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)

        if not cls.name or not cls.error_code:
            raise RuntimeError("Error views must have both `name` and `error_code` defined")

        manager.app.errorhandler(cls.error_code)(cls.as_view(cls.name))
