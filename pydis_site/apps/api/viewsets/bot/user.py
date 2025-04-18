from collections import ChainMap, OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import fields, status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot.infraction import Infraction
from pydis_site.apps.api.models.bot.metricity import Metricity, NotFoundError
from pydis_site.apps.api.models.bot.user import User, UserAltRelationship, UserModSettings
from pydis_site.apps.api.serializers import (
    UserSerializer,
    UserAltRelationshipSerializer,
    UserModSettingsSerializer,
    UserWithAltsSerializer
)


class UserListPagination(PageNumberPagination):
    """Custom pagination class for the User Model."""

    page_size = 2500
    page_size_query_param = "page_size"

    def get_next_page_number(self) -> int | None:
        """Get the next page number."""
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_page_number(self) -> int | None:
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
    ...         'name': "python",
    ...         'display_name': "Python",
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
    - username: username to search for
    - display_name: display name to search for
    - discriminator: discriminator to search for
    - page_size: number of Users in one page, defaults to 10,000
    - page: page number

    #### Status codes
    - 200: returned on success

    ### GET /bot/users/<snowflake:int>
    Gets a single user by ID.

    #### Response format
    >>> {
    ...     'alts': [
    ...         {
    ...             'actor': 1234,
    ...             # Note that alt relationships are not transitive.
    ...             'alts': [409107086526644234, 9012571029],
    ...             'context': "Testing account",
    ...             'source': 409107086526644234,
    ...             'target': 128025
    ...         },
    ...         # ...
    ...     ],
    ...     'id': 409107086526644234,
    ...     'name': "python",
    ...     'display_name': "Python",
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

    ### GET /bot/users/<snowflake:int>/metricity_data
    Gets metricity data for a single user by ID.

    #### Response format
    >>> {
    ...    "joined_at": "2020-10-06T21:54:23.540766",
    ...    "total_messages": 2,
    ...    "voice_banned": False,
    ...    "activity_blocks": 1
    ...}

    #### Status codes
    - 200: returned on success
    - 404: if a user with the given `snowflake` could not be found

    ### GET /bot/users/<snowflake:int>/metricity_review_data
    Gets metricity data for a single user's review by ID.

    #### Response format
    >>> {
    ...     'joined_at': '2020-08-26T08:09:43.507000',
    ...     'top_channel_activity': [['off-topic', 15],
    ...                              ['talent-pool', 4],
    ...                              ['defcon', 2]],
    ...     'total_messages': 22
    ... }

    #### Status codes
    - 200: returned on success
    - 404: if a user with the given `snowflake` could not be found

    ### POST /bot/users/metricity_activity_data
    Returns a mapping of user ID to message count in a given period for
    the given user IDs.

    #### Required Query Parameters
    - days: how many days into the past to count message from.

    #### Request Format
    >>> [
    ...     409107086526644234,
    ...     493839819168808962
    ... ]

    #### Response format
    >>> {
    ...     "409107086526644234": 54,
    ...     "493839819168808962": 0
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if request body or query parameters were missing or invalid

    ### POST /bot/users
    Adds a single or multiple new users.
    The roles attached to the user(s) must be roles known by the site.
    Users that already exist in the database will be skipped.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'display_name': str,
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
    ...     'display_name': str,
    ...     'discriminator': int,
    ...     'roles': List[int],
    ...     'in_guild': bool
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the user with the given `snowflake` could not be found

    ### PATCH /bot/users/<snowflake:int>
    Update the user with the given `snowflake`. All fields in the request body
    are optional.  Note that editing the `'alts'` field is not possible this
    way, use the `alts` endpoint documented below for this.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'display_name': str,
    ...     'discriminator': int,
    ...     'roles': List[int],
    ...     'in_guild': bool
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the user with the given `snowflake` could not be found

    ### POST /bot/users/<snowflake:int>/alts
    Add the alternative account given in the request body to the alternative
    accounts for the given user snowflake. Users will be linked symmetrically.

    #### Request body
    >>> {
    ...     # The target alternate account to associate the user (from the URL) with.
    ...     'target': int,
    ...     # A description for why this relationship was established.
    ...     'context': str,
    ...     # The moderator that associated the accounts together.
    ...     'actor': int
    ... }

    #### Status codes
    - 204: returned on success
    - 400: if the request body was invalid, including if the user in the
      request body could not be found in the database
    - 404: if the user with the given `snowflake` could not be found

    ### PATCH /bot/users/<snowflake:int>/alts
    Update the context of the given alt account on the given user with the
    context specified in the request body.

    #### Request body
    >>> {
    ...     'context': str,
    ...     'target': int
    ... }

    #### Status codes
    - 204: returned on success
    - 400: if the request body was invalid, including if the alternate
      account could not be found as an associated account with the parent
      user account record
    - 404: if the user with the given `snowflake` could not be found

    ### DELETE /bot/users/<snowflake:int>/alts
    Remove the alternative account given in the request body from the
    alternative accounts of the given user snowflake. The request body contains
    the user ID to remove from the association to this user, as a plain
    integer. Users will be linked symmetrically. Returns the updated user.

    #### Request body
    >>> int

    #### Status codes
    - 204: returned on success
    - 400: if the user in the request body was not found as an alt account
    - 404: if the user with the given `snowflake` could not be found

    ### BULK PATCH /bot/users/bulk_patch
    Update users with the given `ids` and `details`. `id` field and at least
    one other field is mandatory. Note that editing the `'alts'` field is not
    possible using this endpoint.

    #### Request body
    >>> [
    ...     {
    ...         'id': int,
    ...         'name': str,
    ...         'display_name': str,
    ...         'discriminator': int,
    ...         'roles': List[int],
    ...         'in_guild': bool
    ...     },
    ...     {
    ...         'id': int,
    ...         'name': str,
    ...         'display_name': str,
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
    queryset = User.objects.select_related("mod_settings").all().order_by("id")
    pagination_class = UserListPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'discriminator', 'display_name')

    def get_serializer(self, *args, **kwargs) -> ModelSerializer:
        """Customize serializers used based on the requested action."""
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True

        # If we are retrieving a single user, user the expanded serializer
        # which also includes context information for each alternate account.
        if self.action == 'retrieve' and self.detail:
            return UserWithAltsSerializer(*args, **kwargs)

        return super().get_serializer(*args, **kwargs)

    @action(detail=False, methods=["PATCH"], name='user-bulk-patch')
    def bulk_patch(self, request: Request) -> Response:
        """Update multiple User objects in a single request."""
        serializer = self.get_serializer(
            instance=self.get_queryset(),
            data=request.data,
            many=True,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], name='mod-settings-update')
    def mod_settings(self, request: Request, pk: str) -> Response:
        """Update the mod settings for a given user."""
        user = self.get_object()
        maybe_mod_settings = UserModSettings.objects.filter(moderator=user).first()

        mod_settings_data = ChainMap({'moderator': user.id}, request.data)

        if maybe_mod_settings:
            mod_settings = UserModSettingsSerializer(maybe_mod_settings, data=mod_settings_data)
        else:
            mod_settings = UserModSettingsSerializer(data=mod_settings_data)

        mod_settings.is_valid(raise_exception=True)

        mod_settings.save()

        return Response(mod_settings.data, status=status.HTTP_200_OK)

    @mod_settings.mapping.delete
    def delete_mod_settings(self, request: Request, pk: str) -> Response:
        """Delete all moderator settings registered for a user."""
        user = self.get_object()
        maybe_mod_settings = UserModSettings.objects.filter(moderator=user).first()

        if not maybe_mod_settings:
            return Response(status=status.HTTP_204_NO_CONTENT)

        maybe_mod_settings.delete()

        return Response(status=status.HTTP_200_OK)


    @action(detail=True, methods=['POST'], name="Add alternate account",
            url_name='alts', url_path='alts')
    def add_alt(self, request: Request, pk: str) -> Response:
        """Associate the given account to the user's alternate accounts."""
        user_id = self.get_object().id
        source_serializer_data = ChainMap({'source': user_id}, request.data)
        source_serializer = UserAltRelationshipSerializer(data=source_serializer_data)
        source_serializer.is_valid(raise_exception=True)

        # This code is somewhat vulnerable to a race condition, in case the first validation
        # from above passes and directly before validating again, one of the users that
        # are referenced here are deleted. Unfortunately, since Django on its own does not
        # query in "both directions", we just need to live with a race condition for validation.
        # For inserts atomicity is guaranteed as we run it in a transaction.
        target_id = source_serializer.validated_data['target'].id
        target_serializer_data = ChainMap({'source': target_id, 'target': user_id}, request.data)
        target_serializer = UserAltRelationshipSerializer(data=target_serializer_data)
        target_serializer.is_valid(raise_exception=True)  # should not fail, or inconsistent db

        with transaction.atomic():
            try:
                source_serializer.save()
                target_serializer.save()
            except IntegrityError as err:
                if err.__cause__.diag.constraint_name == 'api_useraltrelationship_prevent_alt_to_self':
                    raise ParseError(detail={
                        "source": ["The user may not be an alternate account of itself"]
                    })
                if err.__cause__.diag.constraint_name == 'api_useraltrelationship_unique_relationships':
                    raise ParseError(detail={
                        "source": ["This relationship has already been established"]
                    })

                raise  # pragma: no cover

        return Response(status=status.HTTP_204_NO_CONTENT)

    # See https://www.django-rest-framework.org/api-guide/viewsets/#routing-additional-http-methods-for-extra-actions
    # I would really like to include the alternate account to patch in the URL
    # here, but unfortunately it's not possible to do so because the mapping
    # does not accept arguments, and if I were to use the same @action decorator,
    # it would overwrite the other methods and keep them from working.
    @add_alt.mapping.patch
    def update_alt(self, request: Request, pk: str) -> Response:
        """Update the context of a single alt."""
        for field in ('target', 'context'):
            if field not in request.data:
                raise ParseError(detail={field: ["This field is required."]})

        source = self.get_object()
        target = request.data['target']
        with transaction.atomic():
            associated_accounts = (
                UserAltRelationship.objects
                .filter(Q(source=source, target=target) | Q(source=target, target=source))
                .select_for_update()
            )
            count = associated_accounts.count()
            # Sanity check
            assert count in (0, 2), f"Inconsistent database for alts of {source.id} -> {target}"

            if count == 0:
                raise ParseError(detail={'target': ["User is not an associated alt account"]})

            updated = associated_accounts.update(context=request.data['context'])
            assert updated == 2

        return Response(status=status.HTTP_204_NO_CONTENT)

    @add_alt.mapping.delete
    def remove_alt(self, request: Request, pk: str) -> Response:
        """Disassociate the given account from the user's alternate accounts."""
        user = self.get_object()
        if not isinstance(request.data, int):
            raise ParseError(detail={"non_field_errors": ["Request body should be an integer"]})
        try:
            alt = user.alts.get(id=request.data)
        except ObjectDoesNotExist:
            raise ParseError(detail={
                'non_field_errors': ["Specified account is not a known alternate account of this user"]
            })

        # It is mandatory that this query performs a symmetrical delete,
        # because our custom ManyToManyField through model specifies more than
        # two foreign keys to the user model, causing Django to no longer
        # uphold the symmetry of the model. Correct function is verified by
        # the tests, but in case you end up changing it, make sure that it
        # works as expected!
        user.alts.remove(alt)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True)
    def metricity_data(self, request: Request, pk: str | None = None) -> Response:
        """Request handler for metricity_data endpoint."""
        user = self.get_object()

        has_voice_infraction = Infraction.objects.filter(
            Q(user__id=user.id, active=True),
            Q(type="voice_ban") | Q(type="voice_mute")
        ).exists()

        with Metricity() as metricity:
            try:
                data = metricity.user(user.id)

                data["total_messages"] = metricity.total_messages(user.id)
                data["activity_blocks"] = metricity.total_message_blocks(user.id)

                data["voice_gate_blocked"] = has_voice_infraction
                return Response(data, status=status.HTTP_200_OK)
            except NotFoundError:
                return Response(dict(detail="User not found in metricity"),
                                status=status.HTTP_404_NOT_FOUND)

    @action(detail=True)
    def metricity_review_data(self, request: Request, pk: str | None = None) -> Response:
        """Request handler for metricity_review_data endpoint."""
        user = self.get_object()

        with Metricity() as metricity:
            try:
                data = metricity.user(user.id)
                data["total_messages"] = metricity.total_messages(user.id)
                data["top_channel_activity"] = metricity.top_channel_activity(user.id)
                return Response(data, status=status.HTTP_200_OK)
            except NotFoundError:
                return Response(dict(detail="User not found in metricity"),
                                status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["POST"])
    def metricity_activity_data(self, request: Request) -> Response:
        """Request handler for metricity_activity_data endpoint."""
        if "days" in request.query_params:
            try:
                days = int(request.query_params["days"])
            except ValueError:
                raise ParseError(detail={
                    "days": ["This query parameter must be an integer."]
                })
        else:
            raise ParseError(detail={
                "days": ["This query parameter is required."]
            })

        user_id_list_validator = fields.ListField(
            child=fields.IntegerField(min_value=0),
            allow_empty=False
        )
        user_ids = [
            str(user_id) for user_id in
            user_id_list_validator.run_validation(request.data)
        ]

        with Metricity() as metricity:
            data = metricity.total_messages_in_past_n_days(user_ids, days)

        default_data = {user_id: 0 for user_id in user_ids}
        response_data = default_data | dict(data)
        return Response(response_data, status=status.HTTP_200_OK)
