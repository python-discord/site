from collections import ChainMap

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot import Nomination
from pydis_site.apps.api.serializers import NominationSerializer


class NominationViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """
    View providing CRUD operations on helper nominations done through the bot.

    ## Routes
    ### GET /bot/nominations
    Retrieve all nominations.
    May be filtered and ordered by the query parameters.

    #### Query parameters
    - **active** `bool`: whether the nomination is still active
    - **actor__id** `int`: snowflake of the user who nominated the user
    - **user__id** `int`: snowflake of the user who received the nomination
    - **ordering** `str`: comma-separated sequence of fields to order the returned results

    Invalid query parameters are ignored.

    #### Response format
    >>> [
    ...     {
    ...         'id': 1,
    ...         'active': false,
    ...         'actor': 336843820513755157,
    ...         'reason': 'They know how to explain difficult concepts',
    ...         'user': 336843820513755157,
    ...         'inserted_at': '2019-04-25T14:02:37.775587Z',
    ...         'end_reason': 'They were helpered after a staff-vote',
    ...         'ended_at': '2019-04-26T15:12:22.123587Z'
    ...     }
    ... ]

    #### Status codes
    - 200: returned on success

    ### GET /bot/nominations/<id:int>
    Retrieve a single nomination by ID.

    ### Response format
    >>> {
    ...     'id': 1,
    ...     'active': true,
    ...     'actor': 336843820513755157,
    ...     'reason': 'They know how to explain difficult concepts',
    ...     'user': 336843820513755157,
    ...     'inserted_at': '2019-04-25T14:02:37.775587Z',
    ...     'end_reason': 'They were helpered after a staff-vote',
    ...     'ended_at': '2019-04-26T15:12:22.123587Z'
    ... }

    ### Status codes
    - 200: returned on succes
    - 404: returned if a nomination with the given `id` could not be found

    ### POST /bot/nominations
    Create a new, active nomination returns the created nominations.
    The `user`, `reason` and `actor` fields are required and the `user`
    and `actor` need to know by the site. Providing other valid fields
    is not allowed and invalid fields are ignored. A `user` is only
    allowed one active nomination at a time.

    #### Request body
    >>> {
    ...     'actor': 409107086526644234
    ...     'reason': 'He would make a great helper',
    ...     'user': 409107086526644234
    ... }

    ### Response format
    See `GET /bot/nominations/<id:int>`

    #### Status codes
    - 201: returned on success
    - 400: returned on failure for one of the following reasons:
        - A user already has an active nomination;
        - The `user` or `actor` are unknown to the site;
        - The request contained a field that cannot be set at creation.

    ### PATCH /bot/nominations/<id:int>
    Update the nomination with the given `id` and return the updated nomination.
    For active nominations, only the `reason` may be updated; for inactive
    nominations, both the `reason` and `end_reason` may be updated.

    #### Request body
    >>> {
    ...     'reason': 'He would make a great helper',
    ...     'end_reason': 'He needs some time to mature his Python knowledge'
    ... }

    ### Response format
    See `GET /bot/nominations/<id:int>`

    ## Status codes
    - 200: returned on success
    - 400: if a field in the request body is invalid or disallowed
    - 404: if an infraction with the given `id` could not be found

    ### PATCH /bot/nominations/<id:int>/end_nomination
    Ends an active nomination and returns the updated nomination.

    The `end_reason` field is the only allowed and required field
    for this operation. The nomination will automatically be marked as
    `active = false` and the datetime of this operation will be added to
    the `ended_at` field.

    #### Request body
    >>> {
    ...     'end_reason': 'He needs some time to mature his Python knowledge'
    ... }

    ### Response format
    See `GET /bot/nominations/<id:int>`

    #### Status codes
    - 200: returned on success
    - 400: returned on failure for the following reasons:
        - `end_reason` is missing from the request body;
        - Any other field is present in the request body;
        - The nomination was already inactiive.
    - 404: if an infraction with the given `id` could not be found
    """
    serializer_class = NominationSerializer
    queryset = Nomination.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('user__id', 'actor__id', 'active')
    frozen_fields = ('id', 'actor', 'inserted_at', 'user', 'ended_at', 'active')
    frozen_on_create = ('ended_at', 'end_reason', 'active', 'inserted_at')

    def create(self, request, *args, **kwargs):
        """
        DRF method for creating a Nomination.

        Called by the Django Rest Framework in response to the corresponding HTTP request.
        """
        for field in request.data:
            if field in self.frozen_on_create:
                raise ValidationError({field: ['This field cannot be set at creation.']})

        user_id = request.data.get("user")
        if Nomination.objects.filter(active=True, user__id=user_id).exists():
            raise ValidationError({'active': ['There can only be one active nomination.']})

        serializer = self.get_serializer(
            data=ChainMap(
                request.data,
                {"active": True}
            )
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        """
        DRF method for updating a Nomination.

        Called by the Django Rest Framework in response to the corresponding HTTP request.
        """
        for field in request.data:
            if field in self.frozen_fields:
                raise ValidationError({field: ['This field cannot be updated.']})

        instance = self.get_object()

        if instance.active and request.data.get('end_reason'):
            raise ValidationError(
                {'end_reason': ["An active nomination can't have an unnominate reason."]}
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        DRF action for ending an active nomination.

        Creates an API endpoint /bot/nominations/{id}/end_nomination to end a nomination. See
        the class docstring for documentation.
        """
        for field in request.data:
            if field != "end_reason":
                raise ValidationError({field: ['This field cannot be set at end_nomination.']})

        if "end_reason" not in request.data:
            raise ValidationError(
                {'end_reason': ['This field is required when ending a nomination.']}
            )

        instance = self.get_object()
        if not instance.active:
            raise ValidationError({'active': ['A nomination must be active to be ended.']})

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance.active = False
        instance.ended_at = timezone.now()
        serializer.save()
        instance.save()

        return Response(serializer.data)
