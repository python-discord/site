from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
)
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot import BumpedThread
from pydis_site.apps.api.serializers import BumpedThreadSerializer


class BumpedThreadViewSet(
    GenericViewSet, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, ListModelMixin
):
    """
    View providing CRUD (Minus the U) operations on threads to be bumped.

    ## Routes
    ### GET /bot/bumped-threads
    Returns all BumpedThread items in the database.

    #### Response format
    >>> [
    ...     {
    ...         'thread_id': "941705627405811793",
    ...     },
    ...     ...
    ... ]

    #### Status codes
    - 200: returned on success
    - 401: returned if unauthenticated

    ### GET /bot/bumped-threads/<thread_id:int>
    Returns a specific BumpedThread item from the database.

    #### Response format
    >>> {
    ...     'thread_id': "941705627405811793",
    ... }

    #### Status codes
    - 200: returned on success
    - 404: returned if a BumpedThread with the given thread_id was not found.

    ### POST /bot/bumped-threads
    Adds a single BumpedThread item to the database.

    #### Request body
    >>> {
    ...    'thread_id': int,
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/bumped-threads/<thread_id:int>
    Deletes the BumpedThread item with the given `thread_id`.

    #### Status codes
    - 204: returned on success
    - 404: if a BumpedThread with the given `thread_id` does not exist
    """

    serializer_class = BumpedThreadSerializer
    queryset = BumpedThread.objects.all()
