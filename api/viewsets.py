from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from .models import DocumentationLink, SnakeName
from .serializers import DocumentationLinkSerializer, SnakeNameSerializer


class DocumentationLinkViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    View providing documentation links used in the bot's `Doc` cog.

    ## Routes
    ### GET /bot/documentation-links
    Return all documentation links in the database in the following format:

    >>> [
    ...     {
    ...         'package': 'flask',
    ...         'base_url': 'https://flask.pocoo.org/docs/dev',
    ...         'inventory_url': 'https://flask.pocoo.org/docs/objects.inv'
    ...     },
    ...     # ...
    ... ]

    ### GET /bot/documentation-links/<package:str>
    Look up the documentation object for the given `package`.
    If an entry exists, return data in the following format:

    >>> {
    ...     'package': 'flask',
    ...     'base_url': 'https://flask.pocoo.org/docs/dev',
    ...     'inventory_url': 'https://flask.pocoo.org/docs/objects.inv'
    ... }

    Otherwise, if no entry for the given `package` exists, returns 404.
    """

    queryset = DocumentationLink.objects.all()
    serializer_class = DocumentationLinkSerializer
    lookup_field = 'package'


class SnakeNameViewSet(ViewSet):
    """
    View providing snake names for the bot's snake cog from our first code jam's winners.

    ## Routes
    ### GET /bot/snake-names
    By default, return a single random snake name as JSON in the following format:

    >>> {
    ...     'name': "Python",
    ...     'scientific': "Langus greatus"
    ... }

    If the `get_all` query parameter is given, for example using...
        $ curl api.pythondiscord.local:8000/bot/snake-names?get_all=yes
    ...then the API will return all snake names and scientific names in the database,
    for example:

    >>> [
    ...     {'name': "Python 3", 'scientific': "Langus greatus"},
    ...     {'name': "Python 2", 'scientific': "Langus decentus"}
    ... ]

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
