# coding=utf-8
from flask import Blueprint, render_template
from flask.views import MethodView


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


class ErrorView(BaseView):
    error_code = None  # type: int

    @classmethod
    def setup(cls: "ErrorView", blueprint: Blueprint):
        if not cls.name or not cls.error_code:
            raise RuntimeError("Error views must have both `name` and `error_code` defined")

        blueprint.errorhandler(cls.error_code)(cls.as_view(cls.name))
