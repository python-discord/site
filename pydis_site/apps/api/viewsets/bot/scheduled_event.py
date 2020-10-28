from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot.scheduled_event import ScheduledEvent
from pydis_site.apps.api.serializers import ScheduledEventSerializer


class ScheduledEventViewSet(ModelViewSet):
    """
    View providing CRUD operations on Scheduled User Events.

    ## Routes
    ### GET /bot/scheduled-events
    Returns all scheduled user events.
    Can be filtered with query parameters.

    #### Query parameters
    - **user_event__organizer** `int`: event organizer id
    - **user_event__name** `str`: event name


    #### Response format
    >>> [
    ...     {
    ...         'id': 1,
    ...         'user_event': {
    ...             'name': "Among Us",
    ...             'organizer': 409107086526644234,
    ...             'subscriptions': [
    ...                 409107086526644233,
    ...                 409107086526644232,
    ...                 409107086526644231,
    ...             ],
    ...         }
    ...         'start_time': '2020-10-26T12:00:00Z',
    ...         'end_time': '2020-10-26T14:00:00Z'
    ...     }
    ... ]

    #### Status codes
    - 200: returned on success

    ### GET /bot/scheduled-events/<scheduled_event_id:int>
    Gets a single scheduled user event by id.

    #### Response format
    >>> {
    ...     'id': 1,
    ...     'user_event': {
    ...         'name': "Among Us",
    ...         'organizer': 409107086526644234,
    ...         'subscriptions': [
    ...             409107086526644233,
    ...             409107086526644232,
    ...             409107086526644231,
    ...         ]
    ...     }
    ...     'start_time': '2020-10-26T12:00:00Z',
    ...     'end_time': '2020-10-26T14:00:00Z'
    ... }


    #### Status codes
    - 200: returned on success
    - 404: if a scheduled user event with the given `id` could not be found

    ### POST /bot/scheduled-events
    Adds a single scheduled user event.
    The user event must be known by the site.
    The start and end times should be in ISO format(UTC).

    #### Request body
    >>> {
    ...     'user_event_name': str,
    ...     'start_time': str,
    ...     'end_time': str
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if the user event name is invalid

    ### PUT /bot/scheduled-events/<scheduled_event_id:int>
    Update a scheduled user event with the given `scheduled_event_id`.
    All fields in the request body are required.

    #### Request body
    >>> {
    ...     'user_event_name': str,
    ...     'start_time': str,
    ...     'end_time': str
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the scheduled user event with the given `scheduled_event_id` does not exist

    ### PATCH /bot/scheduled-events/<scheduled_event_id:int>
    Update a user event with the given `event name`.
    All fields in the request body are optional.

    #### Request body
    >>> {
    ...     'user_event_name': str,
    ...     'start_time': str,
    ...     'end_time': str
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the scheduled user event with the given `scheduled_event_id` does not exist

    ### DELETE /bot/scheduled-events/<scheduled_event_id:int>
    Deletes the scheduled user event with the given `scheduled_event_id`.

    #### Status codes
    - 204: returned on success
    - 404: if the user event with the given `scheduled_event_id` is not scheduled
    """

    queryset = ScheduledEvent.objects.select_related("user_event").all()
    serializer_class = ScheduledEventSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ("user_event__organizer", "user_event__name")
