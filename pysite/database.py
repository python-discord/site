# coding=utf-8

import os
from typing import Union, List, Any, Dict, Callable

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
            connect_database: bool=True, coerce: type=None) -> Union[rethinkdb.Cursor, List, Dict, object]:
        if not new_connection:
            result = query.run(self.conn)
        else:
            result = query.run(self.get_connection(connect_database))

        if coerce:
            return coerce(result) if result else coerce()
        return result

    # endregion

    # region: Table wrapper functions

    def insert(self, table_name, *objects,
               durability: str="hard", return_changes: Union[bool, str]=False,
               conflict: Union[str, Callable]="error", **kwargs) -> Union[List, Dict]:
        kwargs["durability"] = durability
        kwargs["return_changes"] = return_changes
        kwargs["conflict"] = conflict

        if return_changes:
            return self.run(
                self.query(table_name).insert(*objects, **kwargs),
                coerce=list
            )
        else:
            return self.run(
                self.query(table_name).insert(*objects, **kwargs),
                coerce=dict
            )

    def get(self, table_name, key) -> Union[Dict[str, Any], None]:

        result = self.run(
            self.query(table_name).get(key)
        )

        return dict(result) if result else None

    def get_all(self, table_name, *keys, index="id") -> List[Any]:
        return self.run(
            self.query(table_name).get_all(*keys, index=index),
            coerce=list
        )

    def index_create(self, table_name, *args, **kwargs) -> bool:
        try:
            self.run(
                self.query(table_name).index_create(*args, **kwargs),
                coerce=dict
            )
            return True
        except rethinkdb.RqlRuntimeError:
            # Index already exists
            return False

    def index_drop(self, table_name, *args) -> bool:
        try:
            self.run(
                self.query(table_name).index_drop(*args),
                coerce=dict
            )
            return True
        except rethinkdb.RqlRuntimeError:
            # Index already exists
            return False

    def index_rename(self, table_name, old_index, new_index, *args, overwrite=False, **kwargs):
        args += (old_index, new_index)
        kwargs["overwrite"] = overwrite

        return self.run(
            self.query(table_name).index_rename(*args, **kwargs),
            coerce=dict
        )

    def index_list(self, table_name, *args):
        return self.run(
            self.query(table_name).index_list(*args),
            coerce=list
        )

    def index_status(self, table_name, *args):
        return self.run(
            self.query(table_name).index_status(*args),
            coerce=list
        )

    def index_wait(self, table_name, *args):
        return self.run(
            self.query(table_name).index_wait(*args),
            coerce=list
        )

    def status(self, table_name, *args):
        return self.run(
            self.query(table_name).status(*args)
        )

    def config(self, table_name, *args):
        return self.run(
            self.query(table_name).config(*args)
        )

    def wait(self, table_name, *args, **kwargs):
        return self.run(
            self.query(table_name).wait(*args, **kwargs)
        )

    def reconfigure(self, table_name, *args, **kwargs):
        return self.run(
            self.query(table_name).reconfigure(*args, **kwargs)
        )

    def rebalance(self, table_name, *args, **kwargs):
        return self.run(
            self.query(table_name).reconfigure(*args, **kwargs)
        )

    def sync(self, table_name, *args):
        return self.run(
            self.query(table_name).sync(*args)
        )

    def grant(self, table_name, *args, **kwargs):
        return self.run(
            self.query(table_name).grant(*args, **kwargs)
        )

    def get_intersecting(self, table_name, *args, **kwargs):
        return self.run(
            self.query(table_name).get_intersecting(*args, **kwargs)
        )

    def get_nearest(self, table_name, *args, **kwargs):
        return self.run(
            self.query(table_name).get_nearest(*args, **kwargs)
        )

    def uuid(self, table_name, *args, **kwargs):
        return self.run(
            self.query(table_name).uuid(*args, **kwargs)
        )

    # endregion

    # region: RqlQuery wrapper functions

    def changes(self, table_name, *args):
        return self.run(
            self.query(table_name).changes(*args)
        )

    def pluck(self, table_name, *args):
        return self.run(
            self.query(table_name).pluck(*args)
        )

    # endregion
