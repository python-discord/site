# coding=utf-8
from _weakref import ref

from flask import Blueprint

from rethinkdb.ast import Table

from pysite.database import RethinkDB


class DBMixin:
    """
    Mixin for classes that make use of RethinkDB. It can automatically create a table with the specified primary
    key using the attributes set at class-level.

    This class is intended to be mixed in alongside one of the other view classes. For example:

    >>> class MyView(APIView, DBMixin):
    ...     name = "my_view"  # Flask internal name for this route
    ...     path = "/my_view"  # Actual URL path to reach this route
    ...     table_name = "my_table"  # Name of the table to create
    ...     table_primary_key = "username"  # Primary key to set for this table

    This class will also work with Websockets:

    >>> class MyWeboscket(WS, DBMixin):
    ...     name = "my_websocket"
    ...     path = "/my_websocket"
    ...     table_name = "my_table"
    ...     table_primary_key = "username"

    You may omit `table_primary_key` and it will be defaulted to RethinkDB's default column - "id".
    """

    table_name = ""  # type: str
    table_primary_key = "id"  # type: str

    @classmethod
    def setup(cls: "DBMixin", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        """
        Set up the view by creating the table specified by the class attributes - this will also deal with multiple
        inheritance by calling `super().setup()` as appropriate.

        :param manager: Instance of the current RouteManager (used to get a handle for the database object)
        :param blueprint: Current Flask blueprint
        """

        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)

        if not cls.table_name:
            raise RuntimeError("Routes using DBViewMixin must define `table_name`")

        cls._db = ref(manager.db)
        manager.db.create_table(cls.table_name, primary_key=cls.table_primary_key)

    @property
    def table(self) -> Table:
        return self.db.query(self.table_name)

    @property
    def db(self) -> RethinkDB:
        return self._db()
