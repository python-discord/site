from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot.filter_list import FilterList
from pydis_site.apps.api.serializers import FilterListSerializer


class FilterListViewSet(ModelViewSet):
    """
    View providing CRUD operations on items allowed or denied by our bot.

    ## Routes
    ### GET /bot/filter-lists
    Returns all filterlist items in the database.

    #### Response format
    >>> [
    ...     {
    ...         'id': "2309268224",
    ...         'created_at': "01-01-2020 ...",
    ...         'updated_at': "01-01-2020 ...",
    ...         'type': "file_format",
    ...         'allowed': 'true',
    ...         'content': ".jpeg",
    ...         'comment': "Popular image format.",
    ...     },
    ...     ...
    ... ]

    #### Status codes
    - 200: returned on success
    - 401: returned if unauthenticated

    ### GET /bot/filter-lists/<id:int>
    Returns a specific FilterList item from the database.

    #### Response format
    >>> {
    ...     'id': "2309268224",
    ...     'created_at': "01-01-2020 ...",
    ...     'updated_at': "01-01-2020 ...",
    ...     'type': "file_format",
    ...     'allowed': 'true',
    ...     'content': ".jpeg",
    ...     'comment': "Popular image format.",
    ... }

    #### Status codes
    - 200: returned on success
    - 404: returned if the id was not found.

    ### GET /bot/filter-lists/get-types
    Returns a list of valid list types that can be used in POST requests.

    #### Response format
    >>> [
    ...     ["GUILD_INVITE","Guild Invite"],
    ...     ["FILE_FORMAT","File Format"],
    ...     ["DOMAIN_NAME","Domain Name"],
    ...     ["FILTER_TOKEN","Filter Token"]
    ... ]

    #### Status codes
    - 200: returned on success

    ### POST /bot/filter-lists
    Adds a single FilterList item to the database.

    #### Request body
    >>> {
    ...    'type': str,
    ...    'allowed': bool,
    ...    'content': str,
    ...    'comment': Optional[str],
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/filter-lists/<id:int>
    Deletes the FilterList item with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a tag with the given `id` does not exist
    """

    serializer_class = FilterListSerializer
    queryset = FilterList.objects.all()

    @action(detail=False, url_path='get-types', methods=["get"])
    def get_types(self, _: Request) -> Response:
        """Get a list of all the types of FilterLists we support."""
        return Response(FilterList.FilterListType.choices)
