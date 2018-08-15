from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import SnakeName
from .serializers import SnakeNameSerializer


class SnakeNameViewSet(ReadOnlyModelViewSet):
    queryset = SnakeName.objects.all()
    serializer_class = SnakeNameSerializer
