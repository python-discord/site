# coding=utf-8
import importlib
import inspect
import os

from flask import Flask, abort, g

import rethinkdb

from pysite.base_route import BaseView, ErrorView, RouteView

__author__ = "Gareth Coles"

DB_HOST = os.environ["RETHINKDB_HOST"]
DB_PORT = os.environ["RETHINKDB_PORT"]
DB_DATABASE = os.environ["RETHINKDB_DATABASE"]
DB_TABLE = os.environ["RETHINKDB_TABLE"]


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
                            cls is not RouteView and
                            BaseView in cls.__mro__
                    ):
                        cls.setup(self.app)
                        print(f"View loaded: {cls.name: <25} ({module.__name__}.{cls_name})")

    def setup_db(self):
        connection = self.get_db_connection(connect_database=False)

        try:
            rethinkdb.db_create(DB_DATABASE).run(connection)
            rethinkdb.db(DB_DATABASE).table_create(DB_TABLE).run(connection)
            print("Database created")
        except rethinkdb.RqlRuntimeError:
            print("Database found")
        finally:
            connection.close()

        self.app.before_request(self.db_before_request)
        self.app.teardown_request(self.db_teardown_request)

    def get_db_connection(self, connect_database=True):
        if connect_database:
            return rethinkdb.connect(host=DB_HOST, port=DB_PORT, db=DB_DATABASE)
        else:
            return rethinkdb.connect(host=DB_HOST, port=DB_PORT)

    def db_before_request(self):
        try:
            # g is the Flask global context object
            g.rdb_conn = self.get_db_connection()
        except rethinkdb.RqlDriverError:
            abort(503, "Database connection could be established.")

    def db_teardown_request(self, _):
        try:
            # g is the Flask global context object
            g.rdb_conn.close()
        except AttributeError:
            pass
