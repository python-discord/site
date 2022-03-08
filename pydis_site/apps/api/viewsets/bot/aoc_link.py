from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
)
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot import AocAccountLink
from pydis_site.apps.api.serializers import AocAccountLinkSerializer


class AocAccountLinkViewSet(
    GenericViewSet, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, ListModelMixin
):
    """
    View providing management for Users who linked their AoC accounts to their Discord Account.

    ## Routes

    ### GET /bot/aoc-account-links
    Returns all the AoC account links

    #### Response format
    >>> [
    ...     {
    ...         "user": 2,
    ...         "aoc_username": "AoCUser1"
    ...     }
    ... ]


    ### GET /bot/aoc-account-links<user__id:int>
    Retrieve a AoC account link by User ID

    #### Response format
    >>>
    ...     {
    ...         "user": 2,
    ...         "aoc_username": "AoCUser1"
    ...     }

    #### Status codes
    - 200: returned on success
    - 404: returned if an AoC account link with the given user__id was not found.

    ### POST /bot/aoc-account-links
    Adds a single AoC account link block

    #### Request body
    >>> {
    ...     'user': int,
    ...     'aoc_username': str
    ... }

    #### Status codes
    - 204: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/aoc-account-links/<user__id:int>
    Deletes the AoC account link item with the given `user__id`.
    #### Status codes
    - 204: returned on success
    - 404: if the AoC account link with the given user__id does not exist

    """

    serializer_class = AocAccountLinkSerializer
    queryset = AocAccountLink.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("user__id",)
