from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot.user_event import UserEvent
from pydis_site.apps.api.serializers import UserEventSerializer


class UserEventViewSet(ModelViewSet):
    """
    View providing CRUD operations on server User Events.

    ## Routes
    ### GET /bot/user-events
    Returns all server user events currently known.
    Can be filtered with query parameters.

    #### Query parameters
    - **organizer** `int`: event organizer id

    #### Response format
    >>> [
    ...     {
    ...         'name': "Among Us",
    ...         'organizer': 409107086526644234,
    ...         'description': "Some description.",
    ...         'message_id: 774294034544852992
    ... ]

    #### Status codes
    - 200: returned on success

    ### GET /bot/user-events/<event_name:str>
    Gets a single user event by name.

    #### Response format

    >>> {
    ...     'name': "Among Us",
    ...     'organizer': 409107086526644234,
    ...     'description': "Some description.",
    ...     'message_id: 774294034544852992
    ... }

    #### Status codes
    - 200: returned on success
    - 404: if a user event with the given `name` could not be found

    ### POST /bot/user-events
    Adds a single user event.
    The organizer's id and subscription user ids must be known by the site.
    The subscriptions field is not mandatory.
    #### Request body
    >>> {
    ...     'name': str,
    ...     'organizer': int,
    ...     'description': str,
    ...     'message_id: int
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if the organizer's id or any subscription user ids is invalid

    ### PUT /bot/user-events/<event_name:str>
    Update a user event with the given `event name`.
    All fields are required.

    #### Request body
    >>> {
    ...     'name': str,
    ...     'organizer': int,
    ...     'description': str,
    ...     'message_id: int
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the user event with the given `event name` could not be found

    ### PATCH /bot/user-events/<event_name:str>
    Update a user event with the given `event name`.
    All fields in the request body are optional.

    #### Request body
    >>> {
    ...     'name': str,
    ...     'organizer': int,
    ...     'description': str,
    ...     'message_id: int
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the user event with the given `event name` could not be found

    ### DELETE /bot/user-events/<event_name:str>
    Deletes a user event with the given `event name`.

    #### Status codes
    - 204: returned on success
    - 404: if the user event with the given `event name` does not exist

    """

    queryset = UserEvent.objects.select_related("organizer")
    serializer_class = UserEventSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    lookup_field = "name__iexact"
    filter_fields = ("organizer",)
