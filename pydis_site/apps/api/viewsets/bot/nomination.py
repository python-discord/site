from collections import ChainMap

from django.http.request import HttpRequest
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
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
    - 200: returned on success
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

    #### Response format
    See `GET /bot/nominations/<id:int>`

    #### Status codes
    - 201: returned on success
    - 400: returned on failure for one of the following reasons:
        - A user already has an active nomination;
        - The `user` or `actor` are unknown to the site;
        - The request contained a field that cannot be set at creation.

    ### PATCH /bot/nominations/<id:int>
    Update or end the nomination with the given `id` and return the updated nomination.

    The PATCH route can be used for three distinct operations:
    1. Updating the `reason` of `active` nomination;
    2. Ending an `active` nomination;
    3. Updating the `end_reason` or `reason` field of an `inactive` nomination.

    While the response format and status codes are the same for all three operations (see
    below), the request bodies vary depending on the operation. For all operations it holds
    that providing other valid fields is not allowed and invalid fields are ignored.

    ### 1. Updating the `reason` of `active` nomination

    #### Request body
    >>> {
    ...     'reason': 'He would make a great helper',
    ... }

    #### Response format
    See `GET /bot/nominations/<id:int>`

    #### Status codes
    - 200: returned on success
    - 400: if a field in the request body is invalid or disallowed
    - 404: if an infraction with the given `id` could not be found

    ### 2. Ending an `active` nomination

    #### Request body
    >>> {
    ...     'active': False
    ...     'end_reason': 'They've been added to the Helpers team',
    ... }

    See operation 1 for the response format and status codes.

    ### 3. Updating the `end_reason` or `reason` field of an `inactive` nomination.

    #### Request body
    >>> {
    ...     'reason': 'Updated reason for this nomination',
    ...     'end_reason': 'Updated end_reason for this nomination',
    ... }

    Note: The request body may contain either or both fields.

    See operation 1 for the response format and status codes.
    """

    serializer_class = NominationSerializer
    queryset = Nomination.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('user__id', 'actor__id', 'active')
    frozen_fields = ('id', 'actor', 'inserted_at', 'user', 'ended_at')
    frozen_on_create = ('ended_at', 'end_reason', 'active', 'inserted_at')

    def create(self, request: HttpRequest, *args, **kwargs) -> Response:
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

    def partial_update(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        DRF method for updating a Nomination.

        Called by the Django Rest Framework in response to the corresponding HTTP request.
        """
        for field in request.data:
            if field in self.frozen_fields:
                raise ValidationError({field: ['This field cannot be updated.']})

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # There are three distinct PATCH scenarios we need to validate.
        if instance.active and 'active' not in data:
            # 1. We're updating an active nomination without ending it.
            if 'end_reason' in data:
                raise ValidationError(
                    {'end_reason': ["An active nomination can't have an end reason."]}
                )

        elif instance.active and not data['active']:
            # 2. We're ending an active nomination.
            if 'reason' in data:
                raise ValidationError(
                    {'reason': ['This field cannot be set when ending a nomination.']}
                )

            if 'end_reason' not in request.data:
                raise ValidationError(
                    {'end_reason': ['This field is required when ending a nomination.']}
                )

            instance.ended_at = timezone.now()

        elif 'active' in data:
            # 3. The `active` field is only allowed when ending a nomination.
            raise ValidationError(
                {'active': ['This field can only be used to end a nomination']}
            )

        serializer.save()

        return Response(serializer.data)
