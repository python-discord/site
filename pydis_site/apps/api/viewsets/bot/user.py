import json

from django.db import connections
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_bulk import BulkCreateModelMixin

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.serializers import UserSerializer


class UserViewSet(BulkCreateModelMixin, ModelViewSet):
    """
    View providing CRUD operations on Discord users through the bot.

    ## Routes
    ### GET /bot/users
    Returns all users currently known.

    #### Response format
    >>> [
    ...     {
    ...         'id': 409107086526644234,
    ...         'name': "Python",
    ...         'discriminator': 4329,
    ...         'roles': [
    ...             352427296948486144,
    ...             270988689419665409,
    ...             277546923144249364,
    ...             458226699344019457
    ...         ],
    ...         'in_guild': True
    ...     }
    ... ]

    #### Status codes
    - 200: returned on success

    ### GET /bot/users/<snowflake:int>
    Gets a single user by ID.

    #### Response format
    >>> {
    ...     'id': 409107086526644234,
    ...     'name': "Python",
    ...     'discriminator': 4329,
    ...     'roles': [
    ...         352427296948486144,
    ...         270988689419665409,
    ...         277546923144249364,
    ...         458226699344019457
    ...     ],
    ...     'in_guild': True
    ... }

    #### Status codes
    - 200: returned on success
    - 404: if a user with the given `snowflake` could not be found

    ### GET /bot/users/<snowflake:int>/metricity_data
    Gets metricity data for a single user by ID.

    #### Response format
    >>> {
    ...    "id": "0",
    ...    "name": "foo",
    ...    "avatar_hash": "bar",
    ...    "joined_at": "2020-10-06T18:17:30.101677",
    ...    "created_at": "2020-10-06T18:17:30.101677",
    ...    "is_staff": False,
    ...    "opt_out": False,
    ...    "bot": False,
    ...    "is_guild": True,
    ...    "is_verified": False,
    ...    "public_flags": {},
    ...    "verified_at": null
    ...}

    #### Status codes
    - 200: returned on success
    - 404: if a user with the given `snowflake` could not be found

    ### POST /bot/users
    Adds a single or multiple new users.
    The roles attached to the user(s) must be roles known by the site.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'discriminator': int,
    ...     'roles': List[int],
    ...     'in_guild': bool
    ... }

    Alternatively, request users can be POSTed as a list of above objects,
    in which case multiple users will be created at once.

    #### Status codes
    - 201: returned on success
    - 400: if one of the given roles does not exist, or one of the given fields is invalid

    ### PUT /bot/users/<snowflake:int>
    Update the user with the given `snowflake`.
    All fields in the request body are required.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'discriminator': int,
    ...     'roles': List[int],
    ...     'in_guild': bool
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the user with the given `snowflake` could not be found

    ### PATCH /bot/users/<snowflake:int>
    Update the user with the given `snowflake`.
    All fields in the request body are optional.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'discriminator': int,
    ...     'roles': List[int],
    ...     'in_guild': bool
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the user with the given `snowflake` could not be found

    ### DELETE /bot/users/<snowflake:int>
    Deletes the user with the given `snowflake`.

    #### Status codes
    - 204: returned on success
    - 404: if a user with the given `snowflake` does not exist


    """

    serializer_class = UserSerializer
    queryset = User.objects

    @action(detail=True)
    def metricity_data(self, request: Request, pk: str = None) -> Response:
        """Request handler for metricity_data endpoint."""
        user = self.get_object()
        column_keys = ["id", "name", "avatar_hash", "joined_at", "created_at", "is_staff",
                       "opt_out", "bot", "is_guild", "is_verified", "public_flags", "verified_at"]
        with connections['metricity'].cursor() as cursor:
            query = f"SELECT {','.join(column_keys)} FROM users WHERE id = '%s'"
            cursor.execute(query, [user.id])
            values = cursor.fetchone()
            data = dict(zip(column_keys, values))
            data["public_flags"] = json.loads(data["public_flags"])
            return Response(data, status=status.HTTP_200_OK)
