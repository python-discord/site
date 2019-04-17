from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from pydis_site.apps.api.models.bot import SpecialSnake
from pydis_site.apps.api.serializers import SpecialSnakeSerializer


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
