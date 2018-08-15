from rest_framework.serializers import ModelSerializer

from .models import SnakeName


class SnakeNameSerializer(ModelSerializer):
    class Meta:
        model = SnakeName
