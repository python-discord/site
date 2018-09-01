from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet, ViewSet

from .models import DocumentationLink, OffTopicChannelName, SnakeName
from .serializers import DocumentationLinkSerializer, OffTopicChannelNameSerializer, SnakeNameSerializer


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


class OffTopicChannelNameViewSet(DestroyModelMixin, ViewSet):
    """
    View of off-topic channel names used by the bot
    to rotate our off-topic names on a daily basis.

    ## Routes
    ### GET /bot/off-topic-channel-names
    Return all known off-topic channel names from the database.
    If the `random_items` query parameter is given, for example using...
        $ curl api.pythondiscord.local:8000/bot/off-topic-channel-names?random_items=5
    ... then the API will return `5` random items from the database.

    #### Response format
    Return a list of off-topic-channel names:
    >>> [
    ...     "lemons-lemonade-stand",
    ...     "bbq-with-bisk"
    ... ]

    #### Status codes
    - 200: returned on success
    - 400: returned when `random_items` is not a positive integer

    ### POST /bot/off-topic-channel-names
    Create a new off-topic-channel name in the database.
    The name must be given as a query parameter, for example:
        $ curl api.pythondiscord.local:8000/bot/off-topic-channel-names?name=lemons-lemonade-shop

    #### Status codes
    - 201: returned on success
    - 400: if the request body has invalid fields, see the response for details

    ### DELETE /bot/off-topic-channel-names/<name:str>
    Delete the off-topic-channel name with the given `name`.

    #### Status codes
    - 204: returned on success
    - 404: returned when the given `name` was not found

    ## Authentication
    Requires a API token.
    """

    lookup_field = 'name'
    serializer_class = OffTopicChannelNameSerializer

    def get_object(self):
        queryset = self.get_queryset()
        if self.lookup_field not in self.kwargs:
            raise ParseError(detail={
                'name': ["This query parameter is required."]
            })

        name = self.kwargs[self.lookup_field]
        return get_object_or_404(queryset, name=name)

    def get_queryset(self):
        return OffTopicChannelName.objects.all()

    def create(self, request):
        if 'name' in request.query_params:
            create_data = {'name': request.query_params['name']}
            serializer = OffTopicChannelNameSerializer(data=create_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(create_data, status=HTTP_201_CREATED)

        else:
            raise ParseError(detail={
                'name': ["This query parameter is required."]
            })

    def list(self, request):
        if 'random_items' in request.query_params:
            param = request.query_params['random_items']
            try:
                random_count = int(param)
            except ValueError:
                raise ParseError(detail={'random_items': ["Must be a valid integer."]})

            if random_count <= 0:
                raise ParseError(detail={
                    'random_items': ["Must be a positive integer."]
                })

            queryset = self.get_queryset().order_by('?')[:random_count]
            serialized = self.serializer_class(queryset, many=True)
            return Response(serialized.data)

        queryset = self.get_queryset()
        serialized = self.serializer_class(queryset, many=True)
        return Response(serialized.data)


class SnakeNameViewSet(ViewSet):
    """
    View providing snake names for the bot's snake cog from our first code jam's winners.

    ## Routes
    ### GET /bot/snake-names
    By default, return a single random snake name along with its name and scientific name.
    If the `get_all` query parameter is given, for example using...
        $ curl api.pythondiscord.local:8000/bot/snake-names?get_all=yes
    ... then the API will return all snake names and scientific names in the database.

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
