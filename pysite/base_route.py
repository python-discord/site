# coding=utf-8
from flask import Flask, render_template
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
    def setup(cls: "RouteView", app: Flask):
        if not cls.path or not cls.name:
            raise RuntimeError("Route views must have both `path` and `name` defined")

        app.add_url_rule(cls.path, view_func=cls.as_view(cls.name))


class ErrorView(BaseView):
    error_code = None  # type: int

    @classmethod
    def setup(cls: "ErrorView", app: Flask):
        if not cls.name or not cls.error_code:
            raise RuntimeError("Error views must have both `name` and `error_code` defined")

        app._register_error_handler(None, cls.error_code, cls.as_view(cls.name))
