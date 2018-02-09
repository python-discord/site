# coding=utf-8
from flask import Blueprint, jsonify, render_template
from flask.views import MethodView

from pysite.constants import ErrorCodes


class BaseView(MethodView):
    name = None  # type: str

    def render(self, *template_names, **context):
        context["current_page"] = self.name
        context["view"] = self

        return render_template(template_names, **context)


class RouteView(BaseView):
    path = None  # type: str

    @classmethod
    def setup(cls: "RouteView", blueprint: Blueprint):
        if not cls.path or not cls.name:
            raise RuntimeError("Route views must have both `path` and `name` defined")

        blueprint.add_url_rule(cls.path, view_func=cls.as_view(cls.name))


class APIView(RouteView):
    def error(self, error_code: ErrorCodes):
        data = {
            "error_code": error_code.value,
            "error_message": "Unknown error"
        }

        if error_code is ErrorCodes.unknown_route:
            data["error_message"] = "Unknown API route"

        return jsonify(data)


class ErrorView(BaseView):
    error_code = None  # type: int

    @classmethod
    def setup(cls: "ErrorView", blueprint: Blueprint):
        if not cls.name or not cls.error_code:
            raise RuntimeError("Error views must have both `name` and `error_code` defined")

        blueprint.errorhandler(cls.error_code)(cls.as_view(cls.name))
