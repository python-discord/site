from django.http.request import HttpRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot.infraction import Infraction
from pydis_site.apps.api.serializers import (
    ExpandedInfractionSerializer,
    InfractionSerializer
)


class InfractionViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
    DestroyModelMixin
):
    """
    View providing CRUD operations on infractions for Discord users.

    ## Routes
    ### GET /bot/infractions
    Retrieve all infractions.
    May be filtered by the query parameters.

    #### Query parameters
    - **active** `bool`: whether the infraction is still active
    - **actor__id** `int`: snowflake of the user which applied the infraction
    - **hidden** `bool`: whether the infraction is a shadow infraction
    - **search** `str`: regular expression applied to the infraction's reason
    - **type** `str`: the type of the infraction
    - **user__id** `int`: snowflake of the user to which the infraction was applied
    - **ordering** `str`: comma-separated sequence of fields to order the returned results

    Invalid query parameters are ignored.

    #### Response format
    >>> [
    ...     {
    ...         'id': 5,
    ...         'inserted_at': '2018-11-22T07:24:06.132307Z',
    ...         'expires_at': '5018-11-20T15:52:00Z',
    ...         'active': False,
    ...         'user': 172395097705414656,
    ...         'actor': 125435062127820800,
    ...         'type': 'ban',
    ...         'reason': 'He terk my jerb!',
    ...         'hidden': True
    ...     }
    ... ]

    #### Status codes
    - 200: returned on success

    ### GET /bot/infractions/<id:int>
    Retrieve a single infraction by ID.

    #### Response format
    See `GET /bot/infractions`.

    #### Status codes
    - 200: returned on success
    - 404: if an infraction with the given `id` could not be found

    ### POST /bot/infractions
    Create a new infraction and return the created infraction.
    Only `actor`, `type`, and `user` are required.
    The `actor` and `user` must be users known by the site.

    #### Request body
    >>> {
    ...     'active': False,
    ...     'actor': 125435062127820800,
    ...     'expires_at': '5018-11-20T15:52:00+00:00',
    ...     'hidden': True,
    ...     'type': 'ban',
    ...     'reason': 'He terk my jerb!',
    ...     'user': 172395097705414656
    ... }

    #### Response format
    See `GET /bot/infractions`.

    #### Status codes
    - 201: returned on success
    - 400: if a given user is unknown or a field in the request body is invalid

    ### PATCH /bot/infractions/<id:int>
    Update the infraction with the given `id` and return the updated infraction.
    Only `active`, `reason`, and `expires_at` may be updated.

    #### Request body
    >>> {
    ...     'active': True,
    ...     'expires_at': '4143-02-15T21:04:31+00:00',
    ...     'reason': 'durka derr'
    ... }

    #### Response format
    See `GET /bot/infractions`.

    #### Status codes
    - 200: returned on success
    - 400: if a field in the request body is invalid or disallowed
    - 404: if an infraction with the given `id` could not be found

    ### DELETE /bot/infractions/<id:int>
    Delete the infraction with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a infraction with the given `id` does not exist

    ### Expanded routes
    All routes support expansion of `user` and `actor` in responses. To use an expanded route,
    append `/expanded` to the end of the route e.g. `GET /bot/infractions/expanded`.

    #### Response format
    See `GET /bot/users/<snowflake:int>` for the expanded formats of `user` and `actor`. Responses
    are otherwise identical to their non-expanded counterparts.
    """

    serializer_class = InfractionSerializer
    queryset = Infraction.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('user__id', 'actor__id', 'active', 'hidden', 'type')
    search_fields = ('$reason',)
    frozen_fields = ('id', 'inserted_at', 'type', 'user', 'actor', 'hidden')

    def partial_update(self, request: HttpRequest, *_args, **_kwargs) -> Response:
        """Method that handles the nuts and bolts of updating an Infraction."""
        for field in request.data:
            if field in self.frozen_fields:
                raise ValidationError({field: ['This field cannot be updated.']})

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(url_path='expanded', detail=False)
    def list_expanded(self, *args, **kwargs) -> Response:
        """
        DRF method for listing Infraction entries.

        Called by the Django Rest Framework in response to the corresponding HTTP request.
        """
        self.serializer_class = ExpandedInfractionSerializer
        return self.list(*args, **kwargs)

    @list_expanded.mapping.post
    def create_expanded(self, *args, **kwargs) -> Response:
        """
        DRF method for creating an Infraction.

        Called by the Django Rest Framework in response to the corresponding HTTP request.
        """
        self.serializer_class = ExpandedInfractionSerializer
        return self.create(*args, **kwargs)

    @action(url_path='expanded', url_name='detail-expanded', detail=True)
    def retrieve_expanded(self, *args, **kwargs) -> Response:
        """
        DRF method for retrieving a specific Infraction.

        Called by the Django Rest Framework in response to the corresponding HTTP request.
        """
        self.serializer_class = ExpandedInfractionSerializer
        return self.retrieve(*args, **kwargs)

    @retrieve_expanded.mapping.patch
    def partial_update_expanded(self, *args, **kwargs) -> Response:
        """
        DRF method for updating an Infraction.

        Called by the Django Rest Framework in response to the corresponding HTTP request.
        """
        self.serializer_class = ExpandedInfractionSerializer
        return self.partial_update(*args, **kwargs)
