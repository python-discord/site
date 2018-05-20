from weakref import ref

from flask import Blueprint
from rethinkdb.ast import Table

from pysite.database import RethinkDB
from pysite.oauth import OAuthBackend


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

    >>> class MyWebsocket(WS, DBMixin):
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
            super().setup(manager, blueprint)  # pragma: no cover

        cls._db = ref(manager.db)

    @property
    def table(self) -> Table:
        return self.db.query(self.table_name)

    @property
    def db(self) -> RethinkDB:
        return self._db()


class OAuthMixin:
    """
    Mixin for the classes that need access to a logged in user's information. This class should be used
    to grant route's access to user information, such as name, email, id, ect.

    There will almost never be a need for someone to inherit this, as BaseView does that for you.

    This class will add 3 properties to your route:

        * logged_in (bool): True if user is registered with the site, False else wise.

        * user_data (dict): A dict that looks like this:

        {
            "user_id": Their discord ID,
            "username": Their discord username (without discriminator),
            "discriminator": Their discord discriminator,
            "email": Their email, in which is connected to discord
        }

        user_data returns None, if the user isn't logged in.

        * oauth (OAuthBackend): The instance of pysite.oauth.OAuthBackend, connected to the RouteManager.
    """

    @classmethod
    def setup(cls: "OAuthMixin", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)  # pragma: no cover

        cls._oauth = ref(manager.oauth_backend)

    @property
    def logged_in(self) -> bool:
        return self.user_data is not None

    @property
    def user_data(self) -> dict:
        return self.oauth.user_data()

    @property
    def oauth(self) -> OAuthBackend:
        return self._oauth()
