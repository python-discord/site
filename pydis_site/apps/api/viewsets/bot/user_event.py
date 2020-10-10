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
    - **organizer's id**
    - **subscriber's id**

    #### Response format


    #### Response format
    >>> [
    ...     {
    ...         'id': 1,
    ...         'name': "Among Us",
    ...         'organizer': 409107086526644234,
    ...         'subscriptions': [
    ...             409107086526644233,
    ...             409107086526644232,
    ...             409107086526644231,
    ...         ],
    ...     }
    ... ]

    #### Status codes
    - 200: returned on success

    ### GET /bot/user-events/<event_name:str>
    Gets a single user event by name.

    #### Response format
    >>> {
    ...     'id': 1,
    ...     'name': "Among Us",
    ...     'organizer': 409107086526644234,
    ...     'subscriptions': [
    ...         409107086526644233,
    ...         409107086526644232,
    ...         409107086526644231,
    ...     ],
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
    ...     'subscriptions': List[int],
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if the organizer's id or any subscription user ids is invalid

    ### PUT /bot/users/<event_name:str>
    Update a user event with the given `event name`.
    All fields except the subscriptions in the request body are required.

    #### Request body
    >>> {
    ...     'name': str,
    ...     'organizer': int,
    ...     'subscriptions': List[int],
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the user event with the given `event name` could not be found

    ### PATCH /bot/users/<event_name:str>
    Update a user event with the given `event name`.
    All fields in the request body are optional.

    #### Request body
    >>> {
    ...     'name': str,
    ...     'organizer': int,
    ...     'subscriptions': List[int],
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the user event with the given `event name` could not be found

    ### DELETE /bot/users/<event_name:str>
    Deletes a user event with the given `event name`.

    #### Status codes
    - 204: returned on success
    - 404: if the user event with the given `event name` does not exist

    """

    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    lookup_field = "name"
    filter_fields = ("organizer", "subscriptions")
