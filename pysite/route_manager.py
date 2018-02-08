# coding=utf-8
import importlib
import inspect
import os

from flask import Flask

from pysite.base_route import BaseView, ErrorView


class RouteManager:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = os.environ.get("WEBPAGE_SECRET_KEY")

        self.load_views()

    def run(self):
        self.app.run(port=int(os.environ.get("WEBPAGE_PORT")), debug=False)

    def load_views(self, location="pysite/views"):
        for filename in os.listdir(location):
            if os.path.isdir(f"{location}/{filename}"):
                # Recurse if it's a directory; load ALL the views!
                self.load_views(location=f"{location}/{filename}")
                continue

            if filename.endswith(".py") and not filename.startswith("__init__"):
                module = importlib.import_module(f"{location}/{filename}".replace("/", ".")[:-3])

                for cls_name, cls in inspect.getmembers(module):
                    if (
                            inspect.isclass(cls) and
                            cls is not BaseView and
                            cls is not ErrorView and
                            (BaseView in cls.__mro__ or ErrorView in cls.__mro__)
                    ):
                        cls.setup(self.app)
                        print(f"View loaded: {cls.name: <25} ({module.__name__}.{cls_name})")
