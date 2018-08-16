from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import SnakeName
from .serializers import SnakeNameSerializer


class SnakeNameViewSet(ViewSet):
    """
    View of snake names for the bot's snake cog from our first code jam's winners.

    ## Routes
    ### GET /bot/snake-names
    By default, return a single random snake name in the following format:

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
