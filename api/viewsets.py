from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from .models import DocumentationLink, SnakeName
from .serializers import DocumentationLinkSerializer, SnakeNameSerializer


class DocumentationLinkViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
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


class SnakeNameViewSet(ViewSet):
    """
    View providing snake names for the bot's snake cog from our first code jam's winners.

    ## Routes
    ### GET /bot/snake-names
    By default, return a single random snake name along with its name and scientific name.
    If the `get_all` query parameter is given, for example using...
        $ curl api.pythondiscord.local:8000/bot/snake-names?get_all=yes
    ...then the API will return all snake names and scientific names in the database.

    #### Response format
    Without `get_all` query parameter:
    >>> {
    ...     'name': "Python",
    ...     'scientific': "Langus greatus"
    ... }

    If the database is empty for whatever reason, this will return an empty dictionary.

    With `get_all` query parameter:
    >>> [
    ...     {'name': "Python 3", 'scientific': "Langus greatus"},
    ...     {'name': "Python 2", 'scientific': "Langus decentus"}
    ... ]

    #### Status codes
    - 200: returned on success

    ## Authentication
    Requires a API token.
    """

    serializer_class = SnakeNameSerializer

    def get_queryset(self):
        return SnakeName.objects.all()

    def list(self, request):
        if request.query_params.get('get_all'):
            queryset = self.get_queryset()
            serialized = self.serializer_class(queryset, many=True)
            return Response(serialized.data)

        single_snake = SnakeName.objects.order_by('?').first()
        if single_snake is not None:
            body = {
                'name': single_snake.name,
                'scientific': single_snake.scientific
            }

            return Response(body)

        return Response({})
