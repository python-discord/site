from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot.snake_idiom import SnakeIdiom
from pydis_site.apps.api.serializers import SnakeIdiomSerializer


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
