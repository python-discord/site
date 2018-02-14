# coding=utf-8
import os
import random
import string
from functools import wraps

from flask import Blueprint, g, jsonify, render_template, request
from flask.views import MethodView

from rethinkdb.ast import Table

from pysite.constants import ErrorCodes
from pysite.database import RethinkDB


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

    def valid_api_key(f):
        """
        Decorator to check if X-API-Key is valid.
        """
        @wraps(f)
        def has_valid_api_key(*args, **kwargs):
            if not request.headers.get("X-API-Key") == os.environ.get("API_KEY"):
                resp = jsonify({"error_code": 401, "error_message": "Invalid API-Key"})
                resp.status_code = 401
                return resp
            return f(*args, **kwargs)

        return has_valid_api_key

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
        elif error_code is ErrorCodes.missing_parameters:
            data["error_message"] = "Not all required parameters were provided"

        response = jsonify(data)
        response.status_code = http_code
        return response


class DBViewMixin:
    """
    Mixin for views that make use of RethinkDB. It can automatically create a table with the specified primary
    key using the attributes set at class-level.

    This class is intended to be mixed in alongside one of the other view classes. For example:

    >>> class MyView(APIView, DBViewMixin):
    ...     name = "my_view"  # Flask internal name for this route
    ...     path = "/my_view"  # Actual URL path to reach this route
    ...     table_name = "my_table"  # Name of the table to create
    ...     table_primary_key = "username"  # Primary key to set for this table

    You may omit `table_primary_key` and it will be defaulted to RethinkDB's default column - "id".
    """

    table_name = ""  # type: str
    table_primary_key = "id"  # type: str

    @classmethod
    def setup(cls: "DBViewMixin", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        """
        Set up the view by creating the table specified by the class attributes - this will also deal with multiple
        inheritance by calling `super().setup()` as appropriate.

        :param manager: Instance of the current RouteManager (used to get a handle for the database object)
        :param blueprint: Current Flask blueprint
        """

        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)

        if not cls.table_name:
            raise RuntimeError("Routes using DBViewMixin must define `table_name`")

        manager.db.create_table(cls.table_name, primary_key=cls.table_primary_key)

    @property
    def table(self) -> Table:
        return self.db.query(self.table_name)

    @property
    def db(self) -> RethinkDB:
        return g.db


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

        blueprint.errorhandler(cls.error_code)(cls.as_view(cls.name))
