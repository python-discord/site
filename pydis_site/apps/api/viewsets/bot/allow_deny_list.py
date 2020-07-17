from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot.allow_deny_list import AllowDenyList
from pydis_site.apps.api.serializers import AllowDenyListSerializer


class AllowDenyListViewSet(ModelViewSet):
    """
    View providing CRUD operations on items allowed or denied by our bot.

    ## Routes
    ### GET /bot/allow_deny_lists
    Returns all allow and denylist items in the database.

    #### Response format
    >>> [
    ...     {
    ...         'id': "2309268224",
    ...         'created_at': "01-01-2020 ...",
    ...         'updated_at': "01-01-2020 ...",
    ...         'type': "file_format",
    ...         'allowed': 'true',
    ...         'content': ".jpeg",
    ...     },
    ...     ...
    ... ]

    #### Status codes
    - 200: returned on success
    - 401: returned if unauthenticated

    ### GET /bot/allow_deny_lists/<id:int>
    Returns a specific AllowDenyList item from the database.

    #### Response format
    >>> {
    ...     'id': "2309268224",
    ...     'created_at': "01-01-2020 ...",
    ...     'updated_at': "01-01-2020 ...",
    ...     'type': "file_format",
    ...     'allowed': 'true',
    ...     'content': ".jpeg",
    ... }

    #### Status codes
    - 200: returned on success
    - 404: returned if the id was not found.

    ### POST /bot/allow_deny_lists
    Adds a single AllowDenyList item to the database.

    #### Request body
    >>> {
    ...    'type': str,
    ...    'allowed': bool,
    ...    'content': str,
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/allow_deny_lists/<id:int>
    Deletes the AllowDenyList item with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a tag with the given `id` does not exist
    """

    serializer_class = AllowDenyListSerializer
    queryset = AllowDenyList.objects.all()

    @action(detail=False, methods=["get"])
    def get_types(self, _: Request) -> Response:
        """Get a list of all the types of AllowDenyLists we support."""
        return Response(AllowDenyList.AllowDenyListType.choices)
