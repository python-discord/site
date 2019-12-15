from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot.offensive_message import OffensiveMessage
from pydis_site.apps.api.serializers import OffensiveMessageSerializer


class OffensiveMessageViewSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    """
    View providing CRUD access to offensive messages.

    ## Routes
    ### GET /bot/offensive-messages
    Returns all offensive messages in the database.

    #### Response format
    >>> [
    ...     {
    ...         'id': '631953598091100200',
    ...         'channel_id': '291284109232308226',
    ...         'delete_date': '2019-11-01T21:51:15.545000Z'
    ...     },
    ...     ...
    ... ]

    #### Status codes
    - 200: returned on success

    ### POST /bot/offensive-messages
    Create a new offensive message object.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'channel_id': int,
    ...     'delete_date': datetime.datetime  # ISO-8601-formatted date
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if the body format is invalid

    ### DELETE /bot/offensive-messages/<id:int>
    Delete the offensive message object with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a offensive message object with the given `id` does not exist

    ## Authentication
    Requires an API token.
    """

    serializer_class = OffensiveMessageSerializer
    queryset = OffensiveMessage.objects.all()
