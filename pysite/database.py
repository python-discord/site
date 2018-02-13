# coding=utf-8

import os

from flask import abort

import rethinkdb


class RethinkDB:

    def __init__(self, loop_type: str = "gevent"):
        self.host = os.environ.get("RETHINKDB_HOST", "127.0.0.1")
        self.port = os.environ.get("RETHINKDB_PORT", "28016")
        self.database = os.environ.get("RETHINKDB_DATABASE", "pythondiscord")
        self.conn = None

        rethinkdb.set_loop_type(loop_type)

        with self.get_connection(connect_database=False) as conn:
            try:
                rethinkdb.db_create(self.database).run(conn)
                print(f"Database created: {self.database}")
            except rethinkdb.RqlRuntimeError:
                print(f"Database found: {self.database}")

    def get_connection(self, connect_database: bool = True):
        if connect_database:
            return rethinkdb.connect(host=self.host, port=self.port, db=self.database)
        else:
            return rethinkdb.connect(host=self.host, port=self.port)

    def before_request(self):
        try:
            self.conn = self.get_connection()
        except rethinkdb.RqlDriverError:
            abort(503, "Database connection could not be established.")

    def teardown_request(self, _):
        try:
            self.conn.close()
        except AttributeError:
            pass
