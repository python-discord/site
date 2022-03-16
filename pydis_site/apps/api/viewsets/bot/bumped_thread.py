from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot import BumpedThread
from pydis_site.apps.api.serializers import BumpedThreadSerializer


class BumpedThreadViewSet(
    GenericViewSet, CreateModelMixin, DestroyModelMixin, ListModelMixin
):
    """
    View providing CRUD (Minus the U) operations on threads to be bumped.

    ## Routes
    ### GET /bot/bumped-threads
    Returns all BumpedThread items in the database.

    #### Response format
    >>> list[int]

    #### Status codes
    - 200: returned on success
    - 401: returned if unauthenticated

    ### GET /bot/bumped-threads/<thread_id:int>
    Returns whether a specific BumpedThread exists in the database.

    #### Status codes
    - 204: returned on success
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

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        DRF method for checking if the given BumpedThread exists.

        Called by the Django Rest Framework in response to the corresponding HTTP request.
        """
        self.get_object()
        return Response(status=204)
