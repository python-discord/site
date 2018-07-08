import logging
import os
from typing import Any, Callable, Dict, Iterator, List, Optional, Union
import re

import rethinkdb
from rethinkdb.ast import RqlMethodQuery, Table, UserError
from rethinkdb.net import DefaultConnection
from werkzeug.exceptions import ServiceUnavailable

from pysite.tables import TABLES

STRIP_REGEX = re.compile(r"<[^<]+?>")
WIKI_TABLE = "wiki"


class RethinkDB:

    def __init__(self, loop_type: Optional[str] = "gevent"):
        self.host = os.environ.get("RETHINKDB_HOST", "127.0.0.1")
        self.port = os.environ.get("RETHINKDB_PORT", "28015")
        self.database = os.environ.get("RETHINKDB_DATABASE", "pythondiscord")
        self.log = logging.getLogger(__name__)
        self.conn = None

        if loop_type:
            rethinkdb.set_loop_type(loop_type)

        with self.get_connection() as self.conn:
            try:
                rethinkdb.db_create(self.database).run(self.conn)
                self.log.debug(f"Database created: '{self.database}'")
            except rethinkdb.RqlRuntimeError:
                self.log.debug(f"Database found: '{self.database}'")

    def create_tables(self) -> List[str]:
        """
        Creates whichever tables exist in the TABLES
        constant if they don't already exist in the database.

        :return: a list of the tables that were created.
        """
        created = []

        for table, obj in TABLES.items():
            if self.create_table(table, obj.primary_key):
                created.append(table)

        return created

    def get_connection(self, connect_database: bool = True) -> DefaultConnection:
        """
        Grab a connection to the RethinkDB server, optionally without selecting a database

        :param connect_database: Whether to immediately connect to the database or not
        """

        if connect_database:
            return rethinkdb.connect(host=self.host, port=self.port, db=self.database)
        else:
            return rethinkdb.connect(host=self.host, port=self.port)

    def before_request(self):
        """
        Flask pre-request callback to set up a connection for the duration of the request
        """

        try:
            self.conn = self.get_connection()
        except rethinkdb.RqlDriverError:
            raise ServiceUnavailable("Database connection could not be established.")

    def teardown_request(self, _):
        """
        Flask post-request callback to close a previously set-up connection

        :param _: Exception object, not used here
        """

        try:
            self.conn.close()
        except AttributeError:
            pass

    # region: Convenience wrappers

    def create_table(self, table_name: str, primary_key: str = "id", durability: str = "hard", shards: int = 1,
                     replicas: Union[int, Dict[str, int]] = 1, primary_replica_tag: Optional[str] = None) -> bool:
        """
        Attempt to create a new table on the current database

        :param table_name: The name of the table to create
        :param primary_key: The name of the primary key - defaults to "id"
        :param durability: "hard" (the default) to write the change immediately, "soft" otherwise
        :param shards: The number of shards to span the table over - defaults to 1
        :param replicas: See the RethinkDB documentation relating to replicas
        :param primary_replica_tag: See the RethinkDB documentation relating to replicas

        :return: True if the table was created, False if it already exists
        """

        with self.get_connection() as conn:
            all_tables = rethinkdb.db(self.database).table_list().run(conn)
            self.log.debug(f"Call to table_list returned the following list of tables: {all_tables}")

            if table_name in all_tables:
                self.log.debug(f"Table found: '{table_name}' ({len(all_tables)} tables in total)")
                return False

            # Use a kwargs dict because the driver doesn't check the value
            # of `primary_replica_tag` properly; None is not handled
            kwargs = {
                "primary_key": primary_key,
                "durability": durability,
                "shards": shards,
                "replicas": replicas
            }

            if primary_replica_tag is not None:
                kwargs["primary_replica_tag"] = primary_replica_tag

            rethinkdb.db(self.database).table_create(table_name, **kwargs).run(conn)

            self.log.debug(f"Table created: '{table_name}'")
            return True

    def delete(self,
               table_name: str,
               primary_key: Union[str, None] = None,
               durability: str = "hard",
               return_changes: Union[bool, str] = False) -> dict:
        """
        Delete one or all documents from a table. This can only delete
        either the contents of an entire table, or a single document.
        For more complex delete operations, please use self.query.

        :param table_name: The name of the table to delete from. This must be provided.
        :param primary_key: The primary_key to delete from that table. This is optional.
        :param durability: "hard" (the default) to write the change immediately, "soft" otherwise
        :param return_changes: Whether to return a list of changed values or not - defaults to False
        :return: if return_changes is True, returns a dict containing all changes. Else, returns None.
        """

        if primary_key:
            query = self.query(table_name).get(primary_key).delete(
                durability=durability, return_changes=return_changes
            )
        else:
            query = self.query(table_name).delete(
                durability=durability, return_changes=return_changes
            )

        if return_changes:
            return self.run(query, coerce=dict)
        self.run(query)

    def drop_table(self, table_name: str):
        """
        Attempt to drop a table from the database, along with its data

        :param table_name: The name of the table to drop
        :return: True if the table was dropped, False if the table doesn't exist
        """

        with self.get_connection() as conn:
            all_tables = rethinkdb.db(self.database).table_list().run(conn)

            if table_name not in all_tables:
                return False

            rethinkdb.db(self.database).table_drop(table_name).run(conn)
            return True

    def query(self, table_name: str) -> Table:
        """
        Get a RethinkDB table object that you can run queries against

        >>> db = RethinkDB()
        >>> query = db.query("my_table")
        >>> db.run(query.insert({"key": "value"}), coerce=dict)
        {
            "deleted": 0,
            "errors": 0,
            "inserted": 1,
            "replaced": 0,
            "skipped": 0,
            "unchanged": 0
        }

        :param table_name: Name of the table to query against
        :return: The RethinkDB table object for the table
        """

        if table_name not in TABLES:
            self.log.warning(f"Table not declared in tables.py: {table_name}")

        return rethinkdb.table(table_name)

    def run(self, query: Union[RqlMethodQuery, Table], *, new_connection: bool = False,
            connect_database: bool = True, coerce: type = None) -> Union[rethinkdb.Cursor, List, Dict, object]:
        """
        Run a query using a table object obtained from a call to `query()`

        >>> db = RethinkDB()
        >>> query = db.query("my_table")
        >>> db.run(query.insert({"key": "value"}), coerce=dict)
        {
            "deleted": 0,
            "errors": 0,
            "inserted": 1,
            "replaced": 0,
            "skipped": 0,
            "unchanged": 0
        }

        Note that result coercion is very basic, and doesn't really do any magic. If you want to be able to work
        directly with the result of your query, then don't specify the `coerce` argument - the object that you'd
        usually get from the RethinkDB API will be returned instead.

        :param query: The full query to run
        :param new_connection: Whether to create a new connection or use the current request-bound one
        :param connect_database: If creating a new connection, whether to connect to the database immediately
        :param coerce: Optionally, an object type to attempt to coerce the result to

        :return: The result of the operation
        """

        if not new_connection:
            try:
                result = query.run(self.conn)
            except rethinkdb.ReqlDriverError as e:
                if e.message == "Connection is closed.":
                    self.log.warning("Connection was closed, attempting with a new connection...")
                    result = query.run(self.get_connection(connect_database))
                else:
                    raise
        else:
            result = query.run(self.get_connection(connect_database))

        if coerce:
            return coerce(result) if result else coerce()
        return result

    # endregion

    # region: RethinkDB wrapper functions

    def between(self, table_name: str, *, lower: Any = rethinkdb.minval, upper: Any = rethinkdb.maxval,
                index: Optional[str] = None, left_bound: str = "closed", right_bound: str = "open") -> List[
        Dict[str, Any]]:
        """
        Get all documents between two keys

        >>> db = RethinkDB()
        >>> db.between("users", upper=10, index="conquests")
        [
            {"username": "gdude", "conquests": 2},
            {"username": "joseph", "conquests": 5}
        ]
        >>> db.between("users", lower=10, index="conquests")
        [
            {"username": "lemon", "conquests": 15}
        ]
        >>> db.between("users", lower=2, upper=10, index="conquests" left_bound="open")
        [
            {"username": "gdude", "conquests": 2},
            {"username": "joseph", "conquests": 5}
        ]

        :param table_name: The table to get documents from
        :param lower: The lower-bounded value, leave blank to ignore
        :param upper: The upper-bounded value, leave blank to ignore
        :param index: The key or index to check on each document
        :param left_bound: "open" to include documents that exactly match the lower bound, "closed" otherwise
        :param right_bound: "open" to include documents that exactly match the upper bound, "closed" otherwise

        :return: A list of matched documents; may be empty
        """
        return self.run(  # pragma: no cover
            self.query(table_name).between(lower, upper, index=index, left_bound=left_bound, right_bound=right_bound),
            coerce=list
        )

    def changes(self, table_name: str, squash: Union[bool, int] = False, changefeed_queue_size: int = 100_000,
                include_initial: Optional[bool] = None, include_states: bool = False,
                include_types: bool = False) -> Iterator[Dict[str, Any]]:
        """
        A complicated function allowing you to follow a changefeed for a specific table

        This function will not allow you to specify a set of conditions for your changefeed, so you'll
        have to write your own query and run it with `run()` if you need that. If not, you'll just get every
        change for the specified table.

        >>> db = RethinkDB()
        >>> for document in db.changes("my_table", squash=True):
        ...     print(document.get("new_val", {}))

        Documents take the form of a dict with `old_val` and `new_val` fields by default. These are set to a copy of
        the document before and after the change being represented was made, respectively. The format of these dicts
        can change depending on the arguments you pass to the function, however.

        If a changefeed must be aborted (for example, if the table was deleted), a ReqlRuntimeError will be
        raised.

        Note: This function always creates a new connection. This is to prevent you from losing your changefeed
        when the connection used for a request context is closed.

        :param table_name: The name of the table to watch for changes on

        :param squash: How to deal with batches of changes to a single document - False (the default) to send changes
            as they happen, True to squash changes for single objects together and send them as a single change,
            or an int to specify how many seconds to wait for an object to change before batching it

        :param changefeed_queue_size: The number of changes the server will buffer between client reads before it
            starts to drop changes and issues errors - defaults to  100,000

        :param include_initial: If True, the changefeed will start with the initial values of all the documents in
            the table; the results will have `new_val` fields ONLY to start with if this is the case. Note that
            the old values may be intermixed with new changes if you're still iterating through the old values, but
            only as long as the old value for that field has already been sent. If the order of a document you've
            already seen moves it to a part of the group you haven't yet seen, an "unitial" notification is sent, which
            is simply a dict with an `old_val` field set, and not a `new_val` field set. This option defaults to
            False.

        :param include_states: Whether to send special state documents to the changefeed as its state changes. This
            comprises of special documents with only a `state` field, set to a string - the state of the feed. There
            are currently two states - "initializing" and "ready". This option defaults to False.

        :param include_types: If True, each document generated will include a `type` field which states what type
            of change the document represents. This may be "add", "remove", "change", "initial", "uninitial" or
            "state". This option defaults to False.

        :return: A special iterator that will iterate over documents in the changefeed as they're sent. If there is
            no document waiting, this will block the function until there is.
        """
        return self.run(  # pragma: no cover
            self.query(table_name).changes(
                squash=squash, changefeed_queue_size=changefeed_queue_size, include_initial=include_initial,
                include_states=include_states, include_offsets=False, include_types=include_types
            ),
            new_connection=True
        )

    def filter(self, table_name: str, predicate: Callable[[Dict[str, Any]], bool],
               default: Union[bool, UserError] = False) -> List[Dict[str, Any]]:
        """
        Return all documents in a table for which `predicate` returns true.

        The `predicate` argument should be a function that takes a single argument - a single document to check - and
        it should return True or False depending on whether the document should be included.

        >>> def many_conquests(doc):
        ...     '''Return documents with at least 10 conquests'''
        ...     return doc["conquests"] >= 10
        ...
        >>> db = RethinkDB()
        >>> db.filter("users", many_conquests)
        [
            {"username": "lemon", "conquests": 15}
        ]

        :param table_name: The name of the table to get documents for
        :param predicate: The callable to use to filter the documents
        :param default: What to do if a document is missing fields; True to include them, `rethink.error()` to raise
            aa ReqlRuntimeError, or False to skip over the document (the default)
        :return: A list of documents that match the predicate; may be empty
        """

        return self.run(  # pragma: no cover
            self.query(table_name).filter(predicate, default=default),
            coerce=list
        )

    def get(self, table_name: str, key: Any) -> Optional[Dict[str, Any]]:
        """
        Get a single document from a table by primary key

        :param table_name: The name of the table to get the document from
        :param key: The value of the primary key belonging to the document you want

        :return: The document, or None if it wasn't found
        """

        result = self.run(  # pragma: no cover
            self.query(table_name).get(key)
        )

        return dict(result) if result else None  # pragma: no cover

    def get_all(self, table_name: str, *keys: str, index: str = "id") -> List[Any]:
        """
        Get a list of documents matching a set of keys, on a specific index

        :param table_name: The name of the table to get documents from
        :param keys: The key values to match against
        :param index: The name of the key or index to match on

        :return: A list of matching documents; may be empty if no matches were made
        """

        if keys:
            return self.run(  # pragma: no cover
                self.query(table_name).get_all(*keys, index=index),
                coerce=list
            )
        else:
            return self.run(
                self.query(table_name),
                coerce=list
            )

    def insert(self, table_name: str, *objects: Dict[str, Any],
               durability: str = "hard",
               return_changes: Union[bool, str] = False,
               conflict: Union[  # Any of...
                   str, Callable[  # ...str, or a callable that...
                       [Dict[str, Any], Dict[str, Any]],  # ...takes two dicts with string keys and any values...
                       Dict[str, Any]  # ...and returns a dict with string keys and any values
                   ]
               ] = "error") -> Dict[str, Any]:  # flake8: noqa
        """
        Insert an object or a set of objects into a table

        :param table_name: The name of the table to insert into
        :param objects: The objects to be inserted into the table
        :param durability: "hard" (the default) to write the change immediately, "soft" otherwise
        :param return_changes: Whether to return a list of changed values or not - defaults to False
        :param conflict: What to do in the event of a conflict - "error", "replace" and "update" are included, but
            you can also provide your own function in order to handle conflicts yourself. If you do this, the function
            should take two arguments (the old document and the new one), and return a single document to replace both.

        :return: A dict detailing the operations run
        """

        query = self.query(table_name).insert(
            objects, durability=durability, return_changes=return_changes, conflict=conflict
        )

        return self.run(query, coerce=dict)

    def map(self, table_name: str, func: Callable):
        """
        Map a function over every document in a table, with the possibility of modifying it

        As an example, you could do the following to rename the "id" field to "user_id" for all documents
        in the "users" table.

        >>> db = RethinkDB()
        >>> db.map(
        ...     "users",
        ...     lambda doc: doc.merge({"user_id": doc["id"]}).without("id")
        ... )

        :param table_name: The name of the table to map the function over
        :param func: A callable that takes a single argument

        :return: Unknown, needs more testing
        """

        return self.run(  # pragma: no cover
            self.query(table_name).map(func),
            coerce=list
        )

    def pluck(self, table_name: str, *selectors: Union[str, Dict[str, Union[List, Dict]]]) -> List[Dict[str, Any]]:
        """
        Get a list of values for a specific set of keys for every document in the table; this can include
        nested values

        >>> db = RethinkDB()
        >>> db.pluck("users", "username", "password")  # Select a flat document
        [
            {"username": "lemon", "password": "hunter2"}
        ]
        >>> db.pluck("users", {"posts": ["title"]})  # Select from nested documents
        [
            {
                "posts": [
                    {"title": "New website!"}
                ]
            }
        ]

        :param table_name: The table to get values from
        :param selectors: The set of keys to get values for
        :return: A list containing the requested documents, with only the keys requested
        """

        return self.run(  # pragma: no cover
            self.query(table_name).pluck(*selectors),
            coerce=list
        )

    def sample(self, table_name: str, sample_size: int) -> List[Dict[str, Any]]:
        """
        Select a given number of elements from a table at random.

        :param table_name: The name of the table to select from.
        :param sample_size: The number of elements to select.
            If this number is higher than the total amount of items in
            the table, this will return the entire table in random order.

        :return: A list of items from the table.
        """
        return self.run(  # pragma: no cover
            self.query(table_name).sample(sample_size),
            coerce=list
        )

    def sync(self, table_name: str) -> bool:
        """
        Following a set of edits with durability set to "soft", this must be called to save those edits

        :param table_name: The name of the table to sync

        :return: True if the sync was successful; False otherwise
        """
        result = self.run(  # pragma: no cover
            self.query(table_name).sync(),
            coerce=dict
        )

        return result.get("synced", 0) > 0  # pragma: no cover

    def wait(self, table_name: str, wait_for: str = "all_replicas_ready", timeout: int = 0) -> bool:
        """
        Wait until an operation has happened on a specific table; will block the current function

        :param table_name: The name of the table to wait against
        :param wait_for: The operation to wait for; may be "ready_for_outdated_reads",
            "ready_for_reads", "ready_for_writes" or "all_replicas_ready", which is the default
        :param timeout: How long to wait before returning; defaults to 0 (forever)

        :return: True; but may return False if the timeout was reached
        """

        result = self.run(  # pragma: no cover
            self.query(table_name).wait(wait_for=wait_for, timeout=timeout),
            coerce=dict
        )

        return result.get("ready", 0) > 0

    def without(self, table_name: str, *selectors: Union[str, Dict[str, Union[List, Dict]]]):
        """
        The functional opposite of `pluck()`, returning full documents without the specified selectors

        >>> db = RethinkDB()
        >>> db.without("users", "posts")
        [
            {"username": "lemon", "password": "hunter2"}
        ]

        :param table_name: The table to get values from
        :param selectors: The set of keys to exclude
        :return: A list containing the requested documents, without the keys requested
        """

        return self.run(  # pragma: no cover
            self.query(table_name).without(*selectors)
        )
    # endregion
