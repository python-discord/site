import typing
from collections import OrderedDict

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.serializers import UserSerializer


class UserListPagination(PageNumberPagination):
    """Custom pagination class for the User Model."""

    page_size = 10000
    page_size_query_param = "page_size"

    def get_next_page_number(self) -> typing.Optional[int]:
        """Get the next page number."""
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_page_number(self) -> typing.Optional[int]:
        """Get the previous page number."""
        if not self.page.has_previous():
            return None

        page_number = self.page.previous_page_number()
        return page_number

    def get_paginated_response(self, data: list) -> Response:
        """Override method to send modified response."""
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next_page_no', self.get_next_page_number()),
            ('previous_page_no', self.get_previous_page_number()),
            ('results', data)
        ]))


class UserViewSet(ModelViewSet):
    """
    View providing CRUD operations on Discord users through the bot.

    ## Routes
    ### GET /bot/users
    Returns all users currently known with pagination.

    #### Response format
    >>> {
    ...     'count': 95000,
    ...     'next_page_no': "2",
    ...     'previous_page_no': None,
    ...     'results': [
    ...      {
    ...         'id': 409107086526644234,
    ...         'name': "Python",
    ...         'discriminator': 4329,
    ...         'roles': [
    ...             352427296948486144,
    ...             270988689419665409,
    ...             277546923144249364,
    ...             458226699344019457
    ...         ],
    ...         'in_guild': True
    ...     },
    ...     ]
    ... }

    #### Optional Query Parameters
    - page_size: number of Users in one page, defaults to 10,000
    - page: page number

    #### Status codes
    - 200: returned on success

    ### GET /bot/users/<snowflake:int>
    Gets a single user by ID.

    #### Response format
    >>> {
    ...     'id': 409107086526644234,
    ...     'name': "Python",
    ...     'discriminator': 4329,
    ...     'roles': [
    ...         352427296948486144,
    ...         270988689419665409,
    ...         277546923144249364,
    ...         458226699344019457
    ...     ],
    ...     'in_guild': True
    ... }

    #### Status codes
    - 200: returned on success
    - 404: if a user with the given `snowflake` could not be found

    ### POST /bot/users
    Adds a single or multiple new users.
    The roles attached to the user(s) must be roles known by the site.
    Users that already exist in the database will be skipped.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'discriminator': int,
    ...     'roles': List[int],
    ...     'in_guild': bool
    ... }

    Alternatively, request users can be POSTed as a list of above objects,
    in which case multiple users will be created at once. In this case,
    the response is an empty list.

    #### Status codes
    - 201: returned on success
    - 400: if one of the given roles does not exist, or one of the given fields is invalid
    - 400: if multiple user objects with the same id are given

    ### PUT /bot/users/<snowflake:int>
    Update the user with the given `snowflake`.
    All fields in the request body are required.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'discriminator': int,
    ...     'roles': List[int],
    ...     'in_guild': bool
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the user with the given `snowflake` could not be found

    ### PATCH /bot/users/<snowflake:int>
    Update the user with the given `snowflake`.
    All fields in the request body are optional.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'discriminator': int,
    ...     'roles': List[int],
    ...     'in_guild': bool
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the user with the given `snowflake` could not be found

    ### BULK PATCH /bot/users/bulk_patch
    Update users with the given `ids` and `details`.
    `id` field and at least one other field is mandatory.

    #### Request body
    >>> [
    ...     {
    ...         'id': int,
    ...         'name': str,
    ...         'discriminator': int,
    ...         'roles': List[int],
    ...         'in_guild': bool
    ...     },
    ...     {
    ...         'id': int,
    ...         'name': str,
    ...         'discriminator': int,
    ...         'roles': List[int],
    ...         'in_guild': bool
    ...     },
    ... ]

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 400: if multiple user objects with the same id are given
    - 404: if the user with the given id does not exist

    ### DELETE /bot/users/<snowflake:int>
    Deletes the user with the given `snowflake`.

    #### Status codes
    - 204: returned on success
    - 404: if a user with the given `snowflake` does not exist
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = UserListPagination

    def get_serializer(self, *args, **kwargs) -> ModelSerializer:
        """Set Serializer many attribute to True if request body contains a list."""
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True

        return super().get_serializer(*args, **kwargs)

    @action(detail=False, methods=["PATCH"], name='user-bulk-patch')
    def bulk_patch(self, request: Request) -> Response:
        """Update multiple User objects in a single request."""
        queryset = self.get_queryset()
        object_ids = set()
        for data in request.data:
            try:
                if data["id"] in object_ids:
                    # If request data contains users with same ID.
                    raise ValidationError(
                        {"id": [f"User with ID {data['id']} given multiple times."]}
                    )
            except KeyError:
                # If user ID not provided in request body.
                raise ValidationError(
                    {"id": ["This field is required."]}
                )
            object_ids.add(data["id"])

        filtered_instances = queryset.filter(id__in=object_ids)

        serializer = self.get_serializer(
            instance=filtered_instances,
            data=request.data,
            many=True,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
