from rest_framework.serializers import ModelSerializer

from .models import DocumentationLink, OffTopicChannelName, SnakeName


class DocumentationLinkSerializer(ModelSerializer):
    class Meta:
        model = DocumentationLink
        fields = ('package', 'base_url', 'inventory_url')


class OffTopicChannelNameSerializer(ModelSerializer):
    class Meta:
        model = OffTopicChannelName
        fields = ('name',)

    def to_representation(self, obj):
        return obj.name


class SnakeNameSerializer(ModelSerializer):
    class Meta:
        model = SnakeName
        fields = ('name', 'scientific')
