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
    name = None  # type: str

    def render(self, *template_names, **context):
        context["current_page"] = self.name
        context["view"] = self

        return render_template(template_names, **context)


class RouteView(BaseView):
    path = None  # type: str

    @classmethod
    def setup(cls: "RouteView", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)

        if not cls.path or not cls.name:
            raise RuntimeError("Route views must have both `path` and `name` defined")

        blueprint.add_url_rule(cls.path, view_func=cls.as_view(cls.name))


class APIView(RouteView):
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
    table_name = ""  # type: str

    @classmethod
    def setup(cls: "DBViewMixin", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)

        if not cls.table_name:
            raise RuntimeError("Routes using DBViewMixin must define `table_name`")

        manager.db.create_table(cls.table_name)

    @property
    def table(self) -> Table:
        return self.db.query(self.table_name)

    @property
    def db(self) -> RethinkDB:
        return g.db


class ErrorView(BaseView):
    error_code = None  # type: int

    @classmethod
    def setup(cls: "ErrorView", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)

        if not cls.name or not cls.error_code:
            raise RuntimeError("Error views must have both `name` and `error_code` defined")

        blueprint.errorhandler(cls.error_code)(cls.as_view(cls.name))
