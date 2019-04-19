from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot.snake_fact import SnakeFact
from pydis_site.apps.api.serializers import SnakeFactSerializer


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
