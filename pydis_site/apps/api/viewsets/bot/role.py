from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot.role import Role
from pydis_site.apps.api.serializers import RoleSerializer


class RoleViewSet(ModelViewSet):
    """
    View providing CRUD access to the roles on our server.

    This is used by the bot to keep a mirror of our server's roles on the site.

    ## Routes
    ### GET /bot/roles
    Returns all roles in the database.

    #### Response format
    >>> [
    ...     {
    ...         'id': 267628507062992896,
    ...         'name': "Admins",
    ...         'colour': 1337,
    ...         'permissions': 8,
    ...         'position': 1
    ...     }
    ... ]

    #### Status codes
    - 200: returned on success

    ### GET /bot/roles/<snowflake:int>
    Gets a single role by ID.

    #### Response format
    >>> {
    ...     'id': 267628507062992896,
    ...     'name': "Admins",
    ...     'colour': 1337,
    ...     'permissions': 8,
    ...     'position': 1
    ... }

    #### Status codes
    - 200: returned on success
    - 404: if a role with the given `snowflake` could not be found

    ### POST /bot/roles
    Adds a single new role.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'colour': int,
    ...     'permissions': int,
    ...     'position': 1,
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if the body format is invalid

    ### PUT /bot/roles/<snowflake:int>
    Update the role with the given `snowflake`.
    All fields in the request body are required.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'colour': int,
    ...     'permissions': int,
    ...     'position': 1,
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid
    - 404: if a role with the given `snowflake` does not exist

    ### PATCH /bot/roles/<snowflake:int>
    Update the role with the given `snowflake`.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'colour': int,
    ...     'permissions': int,
    ...     'position': 1,
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid
    - 404: if a role with the given `snowflake` does not exist

    ### DELETE /bot/roles/<snowflake:int>
    Deletes the role with the given `snowflake`.

    #### Status codes
    - 204: returned on success
    - 404: if a role with the given `snowflake` does not exist
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
