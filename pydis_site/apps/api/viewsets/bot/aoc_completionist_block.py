from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
)
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot import AocCompletionistBlock
from pydis_site.apps.api.serializers import AocCompletionistBlockSerializer


class AocCompletionistBlockViewSet(
    GenericViewSet, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, ListModelMixin
):
    """
    View providing management for Users blocked from gettign the AoC completionist Role.

    ## Routes

    ### GET /bot/aoc-completionist-blocks/
    Returns all the AoC completionist blocks

    #### Response format
    >>> [
    ...     {
    ...         "user": 2,
    ...         "is_blocked": False,
    ...         "reason": "Too good to be true"
    ...     }
    ... ]


    ### GET /bot/aoc-completionist-blocks/<user__id:int>
    Retrieve a single Block by User ID

    #### Response format
    >>>
    ...     {
    ...         "user": 2,
    ...         "is_blocked": False,
    ...         "reason": "Too good to be true"
    ...     }

    #### Status codes
    - 200: returned on success
    - 404: returned if an AoC completionist block with the given user__id was not found.

    ### POST /bot/aoc-completionist-blocks
    Adds a single AoC completionist block

    #### Request body
    >>> {
    ...     "user": int,
    ...     "is_blocked": bool,
    ...     "reason": string
    ... }

    #### Status codes
    - 204: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/aoc-completionist-blocks/<user__id:int>
    Deletes the AoC Completionist block item with the given `user__id`.

    #### Status codes
    - 204: returned on success
    - 404: if the AoC Completionist block with the given user__id does not exist

    """

    serializer_class = AocCompletionistBlockSerializer
    queryset = AocCompletionistBlock.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("user__id",)
