from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin,
    ListModelMixin, RetrieveModelMixin
)
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet
from rest_framework_bulk import BulkCreateModelMixin

from .models import (
    DocumentationLink, Infraction,
    OffTopicChannelName,
    SnakeFact, SnakeIdiom,
    SnakeName, SpecialSnake,
    Tag, User
)
from .serializers import (
    DocumentationLinkSerializer, ExpandedInfractionSerializer,
    InfractionSerializer, OffTopicChannelNameSerializer,
    SnakeFactSerializer, SnakeIdiomSerializer,
    SnakeNameSerializer, SpecialSnakeSerializer,
    TagSerializer, UserSerializer
)


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


class InfractionViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = InfractionSerializer
    queryset = Infraction.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('user__id', 'actor__id', 'active', 'hidden', 'type')
    search_fields = ('$reason',)
    frozen_fields = ('id', 'inserted_at', 'type', 'user', 'actor', 'hidden')

    def partial_update(self, request, *args, **kwargs):
        for field in request.data:
            if field in self.frozen_fields:
                raise ValidationError({field: ['This field cannot be updated.']})

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(url_path='expanded', detail=False)
    def list_expanded(self, *args, **kwargs):
        self.serializer_class = ExpandedInfractionSerializer
        return self.list(*args, **kwargs)

    @list_expanded.mapping.post
    def create_expanded(self, *args, **kwargs):
        self.serializer_class = ExpandedInfractionSerializer
        return self.create(*args, **kwargs)

    @action(url_path='expanded', url_name='detail-expanded', detail=True)
    def retrieve_expanded(self, *args, **kwargs):
        self.serializer_class = ExpandedInfractionSerializer
        return self.retrieve(*args, **kwargs)

    @retrieve_expanded.mapping.patch
    def partial_update_expanded(self, *args, **kwargs):
        self.serializer_class = ExpandedInfractionSerializer
        return self.partial_update(*args, **kwargs)


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

    def list(self, request):  # noqa
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


class SnakeFactViewSet(ListModelMixin, GenericViewSet):
    """
    View providing snake facts created by the Pydis community in the first code jam.

    ## Routes
    ### GET /bot/snake-facts
    Returns snake facts from the database.

    #### Response format
    >>> [
    ...     {'fact': 'Snakes are dangerous'},
    ...     {'fact': 'Except for Python, we all love it'}
    ... ]

    #### Status codes
    - 200: returned on success

    ## Authentication
    Requires an API token.
    """

    serializer_class = SnakeFactSerializer
    queryset = SnakeFact.objects.all()


class SnakeIdiomViewSet(ListModelMixin, GenericViewSet):
    """
    View providing snake idioms for the snake cog.

    ## Routes
    ### GET /bot/snake-idioms
    Returns snake idioms from the database.

    #### Response format
    >>> [
    ...    {'idiom': 'Sneky snek'},
    ...    {'idiom': 'Snooky Snake'}
    ... ]

    #### Status codes
    - 200: returned on success

    ## Authentication
    Requires an API token
    """

    serializer_class = SnakeIdiomSerializer
    queryset = SnakeIdiom.objects.all()


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

    def list(self, request):  # noqa
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


class SpecialSnakeViewSet(ListModelMixin, GenericViewSet):
    """
    View providing special snake names for our bot's snake cog.

    ## Routes
    ### GET /bot/special-snakes
    Returns a list of special snake names.

    #### Response Format
    >>> [
    ...   {
    ...     'name': 'Snakky sneakatus',
    ...     'info': 'Scary snek',
    ...     'image': 'https://discordapp.com/assets/53ef346458017da2062aca5c7955946b.svg'
    ...   }
    ... ]

    #### Status codes
    - 200: returned on success

    ## Authentication
    Requires an API token.
    """

    serializer_class = SpecialSnakeSerializer
    queryset = SpecialSnake.objects.all()


class TagViewSet(ModelViewSet):
    """
    View providing CRUD operations on tags shown by our bot.

    ## Routes
    ### GET /bot/tags
    Returns all tags in the database.

    #### Response format
    >>> [
    ...     {
    ...         'title': "resources",
    ...         'embed': {
    ...             'content': "Did you really think I'd put something useful here?"
    ...         }
    ...     }
    ... ]

    #### Status codes
    - 200: returned on success

    ### GET /bot/tags/<title:str>
    Gets a single tag by its title.

    #### Response format
    >>> {
    ...     'title': "My awesome tag",
    ...     'embed': {
    ...         'content': "totally not filler words"
    ...     }
    ... }

    #### Status codes
    - 200: returned on success
    - 404: if a tag with the given `title` could not be found

    ### POST /bot/tags
    Adds a single tag to the database.

    #### Request body
    >>> {
    ...     'title': str,
    ...     'embed': dict
    ... }

    The embed structure is the same as the embed structure that the Discord API
    expects. You can view the documentation for it here:
        https://discordapp.com/developers/docs/resources/channel#embed-object

    #### Status codes
    - 201: returned on success
    - 400: if one of the given fields is invalid

    ### PUT /bot/members/<title:str>
    Update the tag with the given `title`.

    #### Request body
    >>> {
    ...     'title': str,
    ...     'embed': dict
    ... }

    The embed structure is the same as the embed structure that the Discord API
    expects. You can view the documentation for it here:
        https://discordapp.com/developers/docs/resources/channel#embed-object

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the tag with the given `title` could not be found

    ### PATCH /bot/members/<title:str>
    Update the tag with the given `title`.

    #### Request body
    >>> {
    ...     'title': str,
    ...     'embed': dict
    ... }

    The embed structure is the same as the embed structure that the Discord API
    expects. You can view the documentation for it here:
        https://discordapp.com/developers/docs/resources/channel#embed-object

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the tag with the given `title` could not be found

    ### DELETE /bot/members/<title:str>
    Deletes the tag with the given `title`.

    #### Status codes
    - 204: returned on success
    - 404: if a tag with the given `title` does not exist
    """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class UserViewSet(BulkCreateModelMixin, ModelViewSet):
    """
    View providing CRUD operations on Discord users through the bot.

    ## Routes
    ### GET /bot/users
    Returns all users currently known.

    #### Response format
    >>> [
    ...     {
    ...         'id': 409107086526644234,
    ...         'avatar': "3ba3c1acce584c20b1e96fc04bbe80eb",
    ...         'name': "Python",
    ...         'discriminator': 4329,
    ...         'roles': [
    ...             352427296948486144,
    ...             270988689419665409,
    ...             277546923144249364,
    ...             458226699344019457
    ...         ],
    ...         'in_guild': True
    ...     }
    ... ]

    #### Status codes
    - 200: returned on success

    ### GET /bot/users/<snowflake:int>
    Gets a single user by ID.

    #### Response format
    >>> {
    ...     'id': 409107086526644234,
    ...     'avatar': "3ba3c1acce584c20b1e96fc04bbe80eb",
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
    ...     'avatar': str,
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
    ...     'avatar': str,
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
    ...     'avatar': str,
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
