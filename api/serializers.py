from rest_framework.serializers import ModelSerializer

from .models import DocumentationLink, SnakeName


class DocumentationLinkSerializer(ModelSerializer):
    class Meta:
        model = DocumentationLink
        fields = ('package', 'base_url', 'inventory_url')


class SnakeNameSerializer(ModelSerializer):
    class Meta:
        model = SnakeName
        fields = ('name', 'scientific')
