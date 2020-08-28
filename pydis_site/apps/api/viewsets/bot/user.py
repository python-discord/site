from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.serializers import UserSerializer


class UserListPagination(PageNumberPagination):
    """Custom pagination class for the User Model."""

    page_size = 10000
    page_size_query_param = "page_size"


class UserViewSet(ModelViewSet):
    """
    View providing CRUD operations on Discord users through the bot.

    ## Routes
    ### GET /bot/users
    Returns all users currently known with pagination.

    #### Response format
    >>> {
    ...     'count': 95000,
    ...     'next': "http://api.pythondiscord.com/bot/users?page=2",
    ...     'previous': None,
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

    #### Query Parameters
    - page_size: Number of Users in one page.
    - page: Page number

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

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'discriminator': int,
    ...     'roles': List[int],
    ...     'in_guild': bool
    ... }

    Alternatively, request users can be POSTed as a list of above objects,
    in which case multiple users will be created at once.

    #### Status codes
    - 201: returned on success
    - 400: if one of the given roles does not exist, or one of the given fields is invalid

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
        """
        Update multiple User objects in a single request.

        ## Route
        ### PATCH /bot/users/bulk_patch
        Update all users with the IDs.
        `id` field is mandatory, rest are optional.

        #### Request body
        >>> [
        ...     {
        ...     'id': int,
        ...     'name': str,
        ...     'discriminator': int,
        ...     'roles': List[int],
        ...     'in_guild': bool
        ...     },
        ...     {
        ...     'id': int,
        ...     'name': str,
        ...     'discriminator': int,
        ...     'roles': List[int],
        ...     'in_guild': bool
        ...     },
        ... ]

        #### Status codes
        - 200: Returned on success.
        - 400: if the request body was invalid, see response body for details.
        """
        queryset = self.get_queryset()
        try:
            object_ids = [item["id"] for item in request.data]
        except KeyError:
            # user ID not provided in request body.
            resp = {
                "Error": "User ID not provided."
            }
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)

        filtered_instances = queryset.filter(id__in=object_ids)

        if filtered_instances.count() != len(object_ids):
            # If all user objects passed in request.body are not present in the database.
            resp = {
                "Error": "User object not found."
            }
            return Response(resp, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(
            instance=filtered_instances,
            data=request.data,
            many=True,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
