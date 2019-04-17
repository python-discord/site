from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin,
    ListModelMixin, RetrieveModelMixin
)
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot.documentation_link import DocumentationLink
from pydis_site.apps.api.serializers import DocumentationLinkSerializer


class DocumentationLinkViewSet(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    """
    View providing management of documentation links used in the bot's `Doc` cog.

    ## Routes
    ### GET /bot/documentation-links
    Retrieve all currently stored entries from the database.

    #### Response format
    >>> [
    ...     {
    ...         'package': 'flask',
    ...         'base_url': 'https://flask.pocoo.org/docs/dev',
    ...         'inventory_url': 'https://flask.pocoo.org/docs/objects.inv'
    ...     },
    ...     # ...
    ... ]

    #### Status codes
    - 200: returned on success

    ### GET /bot/documentation-links/<package:str>
    Look up the documentation object for the given `package`.

    #### Response format
    >>> {
    ...     'package': 'flask',
    ...     'base_url': 'https://flask.pocoo.org/docs/dev',
    ...     'inventory_url': 'https://flask.pocoo.org/docs/objects.inv'
    ... }

    #### Status codes
    - 200: returned on success
    - 404: if no entry for the given `package` exists

    ### POST /bot/documentation-links
    Create a new documentation link object.

    #### Body schema
    >>> {
    ...     'package': str,
    ...     'base_url': URL,
    ...     'inventory_url': URL
    ... }

    #### Status codes
    - 201: returned on success
    - 400: if the request body has invalid fields, see the response for details

    ### DELETE /bot/documentation-links/<package:str>
    Delete the entry for the given `package`.

    #### Status codes
    - 204: returned on success
    - 404: if the given `package` could not be found
    """

    queryset = DocumentationLink.objects.all()
    serializer_class = DocumentationLinkSerializer
    lookup_field = 'package'
