# coding=utf-8
from flask import Flask, render_template
from flask.views import MethodView

__author__ = "Gareth Coles"


class BaseView(MethodView):
    def render(self, *template_names, **context):
        # thin wrapper here in case it needs to be modified later
        return render_template(template_names, **context)


class RouteView(BaseView):
    path = None  #: str
    name = None  #: str

    @classmethod
    def setup(cls: "RouteView", app: Flask):
        if not cls.path or not cls.name:
            raise RuntimeError("Route views must have both `path` and `name` defined")

        app.add_url_rule(cls.path, view_func=cls.as_view(cls.name))


class ErrorView(BaseView):
    name = None  #: str
    error_code = None  #: int

    @classmethod
    def setup(cls: "ErrorView", app: Flask):
        if not cls.name or not cls.error_code:
            raise RuntimeError("Error views must have both `name` and `error_code` defined")

        app._register_error_handler(None, cls.error_code, cls.as_view(cls.name))
