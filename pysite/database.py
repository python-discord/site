# coding=utf-8

import os
from typing import Union

from flask import abort

import rethinkdb
from rethinkdb.ast import RqlMethodQuery, Table


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

    # region: Convenience wrappers

    def create_table(self, table_name: str, *args, **kwargs) -> bool:
        with self.get_connection() as conn:
            try:
                rethinkdb.db(self.database).table_create(table_name, *args, **kwargs).run(conn)
                return True
            except rethinkdb.RqlRuntimeError:
                return False

    def query(self, table_name: str) -> Table:
        return rethinkdb.table(table_name)

    def run(self, query: RqlMethodQuery, *, new_connection: bool=False,
            connect_database: bool=True, coerce: type=None) -> Union[rethinkdb.Cursor, object]:
        if not new_connection:
            result = query.run(self.conn)
        else:
            result = query.run(self.get_connection(connect_database))

        if coerce:
            return coerce(result) if result else coerce()
        return result

    def insert_now(self, table_name, *args):
        return self.run(
            self.query(table_name).insert(*args)
        )

    def get_now(self, table_name, *args):
        return self.run(
            self.query(table_name).get(*args)
        )

    def get_all_now(self, table_name, *args, **kwargs):
        return self.run(
            self.query(table_name).get_all(*args, **kwargs)
        )

    def index_create_now(self, table_name, *args, **kwargs):
        return self.run(
            self.query(table_name).index_create(*args, **kwargs)
        )

    # endregion
