# coding=utf-8
__author__ = 'Joreth Cales'

import os

<<<<<<< HEAD
from flask import abort
=======
from flask import abort, g
>>>>>>> 327f3f1b4b6e53f6aa2093e459c203009b77aa65

import rethinkdb


class RethinkDB:

    def __init__(self):
        connection = self.get_connection(connect_database=False)

        self.host = os.environ.get("RETHINKDB_HOST")
        self.port = os.environ.get("RETHINKDB_PORT")
<<<<<<< HEAD
        self.database = os.environ.get("RETHINKDB_DATABASE")
        self.conn = None

        try:
            rethinkdb.db_create(self.database).run(connection)
            print(f"Database created: {self.database}")
        except rethinkdb.RqlRuntimeError:
            print(f"Database found: {self.database}")
=======
        self.db = os.environ.get("RETHINKDB_DATABASE")

        try:
            rethinkdb.db_create(self.db).run(connection)
            print(f"Database created: {self.db}")
        except rethinkdb.RqlRuntimeError:
            print(f"Database found: {self.db}")
>>>>>>> 327f3f1b4b6e53f6aa2093e459c203009b77aa65
        finally:
            connection.close()

    def get_connection(self, connect_database=True):
        if connect_database:
<<<<<<< HEAD
            return rethinkdb.connect(host=self.host, port=self.port, db=self.database)
=======
            return rethinkdb.connect(host=self.host, port=self.port, db=self.db)
>>>>>>> 327f3f1b4b6e53f6aa2093e459c203009b77aa65
        else:
            return rethinkdb.connect(host=self.host, port=self.port)

    def before_request(self):
        try:
<<<<<<< HEAD
            self.conn = self.get_connection()
        except rethinkdb.RqlDriverError:
            abort(503, "Database connection could not be established.")

    def teardown_request(self, _):
        try:
            self.conn.close()
=======
            # g is the Flask global context object
            g.rdb_conn = self.get_connection()
        except rethinkdb.RqlDriverError:
            abort(503, "Database connection could be established.")

    def teardown_request(self, _):
        try:
            # g is the Flask global context object
            g.rdb_conn.close()
>>>>>>> 327f3f1b4b6e53f6aa2093e459c203009b77aa65
        except AttributeError:
            pass
