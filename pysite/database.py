# coding=utf-8
__author__ = 'Joreth Cales'

import os

from flask import abort, g

import rethinkdb


class RethinkDB:

    def __init__(self):
        connection = self.get_connection(connect_database=False)

        self.host = os.environ.get("RETHINKDB_HOST")
        self.port = os.environ.get("RETHINKDB_PORT")
        self.db = os.environ.get("RETHINKDB_DATABASE")

        try:
            rethinkdb.db_create(self.db).run(connection)
            print(f"Database created: {self.db}")
        except rethinkdb.RqlRuntimeError:
            print(f"Database found: {self.db}")
        finally:
            connection.close()

    def get_connection(self, connect_database=True):
        if connect_database:
            return rethinkdb.connect(host=self.host, port=self.port, db=self.db)
        else:
            return rethinkdb.connect(host=self.host, port=self.port)

    def before_request(self):
        try:
            # g is the Flask global context object
            g.rdb_conn = self.get_connection()
        except rethinkdb.RqlDriverError:
            abort(503, "Database connection could not be established.")

    def teardown_request(self, _):
        try:
            # g is the Flask global context object
            g.rdb_conn.close()
        except AttributeError:
            pass
