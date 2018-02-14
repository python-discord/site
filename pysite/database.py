# coding=utf-8

import os
from typing import Any, Callable, Dict, Iterator, List, Optional, Union

from flask import abort

import rethinkdb
from rethinkdb.ast import RqlMethodQuery, Table, UserError


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
                print(f"Database created: '{self.database}'")
            except rethinkdb.RqlRuntimeError:
                print(f"Database found: '{self.database}'")

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

    def create_table(self, table_name: str, primary_key: str="id", durability: str="hard", shards: int=1,
                     replicas: Union[int, Dict[str, int]]=1, primary_replica_tag: Optional[str]=None) -> bool:
        with self.get_connection() as conn:
            all_tables = rethinkdb.db(self.database).table_list().run(conn)

            if table_name in all_tables:
                print(f"Table found: '{table_name}' ({len(all_tables)} tables in total)")
                return False

            kwargs = {
                "primary_key": primary_key,
                "durability": durability,
                "shards": shards,
                "replicas": replicas
            }

            if primary_replica_tag is not None:
                kwargs["primary_replica_tag"] = primary_replica_tag

            rethinkdb.db(self.database).table_create(table_name, **kwargs).run(conn)

            print(f"Table created: '{table_name}'")
            return True

    def drop_table(self, table_name: str):
        with self.get_connection() as conn:
            try:
                rethinkdb.db(self.database).table_drop(table_name).run(conn)
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

    # region: RethinkDB wrapper functions

    def insert(self, table_name: str, *objects: Dict[str, Any],
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

    def get(self, table_name: str, key: str) -> Union[Dict[str, Any], None]:
        result = self.run(
            self.query(table_name).get(key)
        )

        return dict(result) if result else None

    def get_all(self, table_name: str, *keys: str, index: str="id") -> List[Any]:
        return self.run(
            self.query(table_name).get_all(*keys, index=index),
            coerce=list
        )

    def wait(self, table_name: str, wait_for="all_replicas_ready", timeout=0):
        result = self.run(
            self.query(table_name).wait(wait_for=wait_for, timeout=timeout),
            coerce=dict
        )

        return result.get("ready", 0) > 0

    def sync(self, table_name: str):
        result = self.run(
            self.query(table_name).sync(),
            coerce=dict
        )

        return result.get("synced", 0) > 0

    def changes(self, table_name: str, squash: Union[bool, int]=False, changefeed_queue_size: int=100_000,
                include_initial: Optional[bool]=None, include_states: bool=False, include_offsets: Optional[bool]=None,
                include_types: bool=False) -> Iterator[Dict[str, Any]]:
        return self.run(
            self.query(table_name).changes(
                squash=squash, changefeed_queue_size=changefeed_queue_size, include_initial=include_initial,
                include_states=include_states, include_offsets=include_offsets, include_types=include_types
            )
        )

    def pluck(self, table_name: str, *selectors: str):
        return self.run(
            self.query(table_name).pluck(*selectors)
        )

    def between(self, table_name: str, *, lower: Any=rethinkdb.minval, upper: Any=rethinkdb.maxval,
                index: Optional[str]=None, left_bound: str="closed", right_bound: str ="open") -> List[Dict[str, Any]]:
        return self.run(
            self.query(table_name).between(lower, upper, index=index, left_bound=left_bound, right_bound=right_bound),
            coerce=list
        )

    def filter(self, table_name: str, predicate: Callable[[Dict[str, Any]], bool],
               default: Union[bool, UserError]=False) -> List[Dict[str, Any]]:
        return self.run(
            self.query(table_name).filter(predicate, default=default),
            coerce=list
        )

    # endregion
