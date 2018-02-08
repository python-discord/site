# coding=utf-8
from flask import Flask
from flask.views import MethodView


class BaseView(MethodView):
    path = None  #: str
    name = None  #: str

    @classmethod
    def setup(cls: "BaseView", app: Flask):
        if not cls.path or not cls.name:
            raise RuntimeError("Route views must have both `path` and `name` defined")

        app.add_url_rule(cls.path, view_func=cls.as_view(cls.name))


class ErrorView(MethodView):
    name = None  #: str
    error_code = None  #: int

    @classmethod
    def setup(cls: "ErrorView", app: Flask):
        if not cls.name or not cls.error_code:
            raise RuntimeError("Error views must have both `name` and `error_code` defined")

        app._register_error_handler(None, cls.error_code, cls.as_view(cls.name))
