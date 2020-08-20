from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot.reminder import Reminder
from pydis_site.apps.api.serializers import ReminderSerializer


class ReminderViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    """
    View providing CRUD access to reminders.

    ## Routes
    ### GET /bot/reminders
    Returns all reminders in the database.

    #### Response format
    >>> [
    ...     {
    ...         'active': True,
    ...         'author': 1020103901030,
    ...         'mentions': [
    ...             336843820513755157,
    ...             165023948638126080,
    ...             267628507062992896
    ...         ],
    ...         'content': "Make dinner",
    ...         'expiration': '5018-11-20T15:52:00Z',
    ...         'id': 11,
    ...         'channel_id': 634547009956872193,
    ...         'jump_url': "https://discord.com/channels/<guild_id>/<channel_id>/<message_id>"
    ...     },
    ...     ...
    ... ]

    #### Status codes
    - 200: returned on success

    ### GET /bot/reminders/<id:int>
    Fetches the reminder with the given id.

    #### Response format
    >>>
    ... {
    ...     'active': True,
    ...     'author': 1020103901030,
    ...     'mentions': [
    ...         336843820513755157,
    ...         165023948638126080,
    ...         267628507062992896
    ...     ],
    ...     'content': "Make dinner",
    ...     'expiration': '5018-11-20T15:52:00Z',
    ...     'id': 11,
    ...     'channel_id': 634547009956872193,
    ...     'jump_url': "https://discord.com/channels/<guild_id>/<channel_id>/<message_id>"
    ... }

    #### Status codes
    - 200: returned on success
    - 404: returned when the reminder doesn't exist

    ### POST /bot/reminders
    Create a new reminder.

    #### Request body
    >>> {
    ...     'author': int,
    ...     'mentions': List[int],
    ...     'content': str,
    ...     'expiration': str,  # ISO-formatted datetime
    ...     'channel_id': int,
    ...     'jump_url': str
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if the body format is invalid
    - 404: if no user with the given ID could be found

    ### PATCH /bot/reminders/<id:int>
    Update the user with the given `id`.
    All fields in the request body are optional.

    #### Request body
    >>> {
    ...     'mentions': List[int],
    ...     'content': str,
    ...     'expiration': str  # ISO-formatted datetime
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the body format is invalid
    - 404: if no user with the given ID could be found

    ### DELETE /bot/reminders/<id:int>
    Delete the reminder with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a reminder with the given `id` does not exist

    ## Authentication
    Requires an API token.
    """

    serializer_class = ReminderSerializer
    queryset = Reminder.objects.prefetch_related('author')
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('active', 'author__id')
