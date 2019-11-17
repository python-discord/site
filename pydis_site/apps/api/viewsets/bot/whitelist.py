from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot.whitelist import Whitelist
from pydis_site.apps.api.serializers import WhitelistSerializer


class WhitelistViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    View providing create, list and  delete operations on whitelist shown by our bot.

    ## Routes
    ### GET /bot/whitelist?type=invites
    Returns all whitelisted items for the invites type in the database.

    #### Response format
    >>> [
    ...      {
    ...        "id": 1,
    ...        "type": "invite",
    ...        "whitelisted_item": "123345"
    ...      },
    ...      {
    ...        "id": 2,
    ...        "type": "invite",
    ...        "whitelisted_item": "1223334"
    ...      },
    ...      {
    ...        "id": 3,
    ...        "type": "invite",
    ...        "whitelisted_item": "121232323"
    ...      }
    ... ]

    #### Status codes
    - 200: returned on success

    ### POST /bot/whitelist
    Adds a single whitelist item to the database.

    #### Request body
    >>> {
    ...     'type': str,
    ...     'whitelisted_item': str
    ... }


    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### DELETE /bot/whitelist/<id:int>
    Deletes the entry with the given `id`.

    #### Status codes
    - 204: returned on success
    - 404: if a tag with the given `id` does not exist
    """

    serializer_class = WhitelistSerializer
    queryset = Whitelist.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('type', )
