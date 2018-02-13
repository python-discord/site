# coding=utf-8
import importlib
import inspect
import os

from flask import Blueprint, Flask, g

from pysite.base_route import APIView, BaseView, ErrorView, RouteView
from pysite.database import RethinkDB
from pysite.logs import Logs

TEMPLATES_PATH = "../templates"
STATIC_PATH = "../static"


class RouteManager:
    def __init__(self):

        # Set up the app and the database
        self.app = Flask(
            __name__, template_folder=TEMPLATES_PATH, static_folder=STATIC_PATH, static_url_path="/static",
        )

        # Store logger in the Flask global context
        self.log = Logs(self.app)
        with self.app.app_context():
            g.log = self.log  # type: RethinkDB

        self.db = RethinkDB()
        self.app.secret_key = os.environ.get("WEBPAGE_SECRET_KEY", "super_secret")
        self.app.config["SERVER_NAME"] = os.environ.get("SERVER_NAME", "pythondiscord.com:8080")
        self.app.before_request(self.db.before_request)
        self.app.teardown_request(self.db.teardown_request)

        # Store the database in the Flask global context
        with self.app.app_context():
            g.db = self.db  # type: RethinkDB

        # Load the main blueprint
        self.main_blueprint = Blueprint("main", __name__)
        self.log.debug(f"Loading Blueprint: {self.main_blueprint.name}")
        self.load_views(self.main_blueprint, "pysite/views/main")
        self.app.register_blueprint(self.main_blueprint)
        self.log.debug("")

        # Load the subdomains
        self.subdomains = ['api', 'staff']

        for sub in self.subdomains:
            self.sub_blueprint = Blueprint(sub, __name__, subdomain=sub)

            self.log.debug(f"Loading Blueprint: {self.sub_blueprint.name}")
            self.load_views(self.sub_blueprint, f"pysite/views/{sub}")
            self.app.register_blueprint(self.sub_blueprint)
            self.log.debug("")

    def run(self):
        self.app.run(
            host=os.environ.get("FLASK_HOST", "127.0.0.1"),
            port=int(os.environ.get("WEBPAGE_PORT", 8080)),
            debug="FLASK_DEBUG" in os.environ
        )

    def load_views(self, blueprint, location="pysite/views"):
        for filename in os.listdir(location):
            if os.path.isdir(f"{location}/{filename}"):
                # Recurse if it's a directory; load ALL the views!
                self.load_views(blueprint, location=f"{location}/{filename}")
                continue

            if filename.endswith(".py") and not filename.startswith("__init__"):
                module = importlib.import_module(f"{location}/{filename}".replace("/", ".")[:-3])

                for cls_name, cls in inspect.getmembers(module):
                    if (
                            inspect.isclass(cls) and
                            cls is not BaseView and
                            cls is not ErrorView and
                            cls is not RouteView and
                            cls is not APIView and
                            BaseView in cls.__mro__
                    ):
                        cls.setup(blueprint)
                        self.log.debug(f">> View loaded: {cls.name: <15} ({module.__name__}.{cls_name})")
