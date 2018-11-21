from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, ValidationError
from rest_framework_bulk import BulkSerializerMixin

from .models import (
    DocumentationLink, Infraction,
    OffTopicChannelName,
    Role, SnakeFact,
    SnakeIdiom, SnakeName,
    SpecialSnake, Tag, User
)


class DocumentationLinkSerializer(ModelSerializer):
    class Meta:
        model = DocumentationLink
        fields = ('package', 'base_url', 'inventory_url')


class InfractionSerializer(ModelSerializer):
    class Meta:
        model = Infraction
        fields = (
            'id', 'inserted_at', 'expires_at', 'active', 'user', 'actor', 'type', 'reason', 'hidden'
        )

    def validate(self, attrs):
        infr_type = attrs.get('type')

        expires_at = attrs.get('expires_at')
        if expires_at and infr_type in ('kick', 'warning'):
            raise ValidationError({'expires_at': [f'{infr_type} infractions cannot expire.']})

        hidden = attrs.get('hidden')
        if hidden and infr_type in ('superstar',):
            raise ValidationError({'hidden': [f'{infr_type} infractions cannot be hidden.']})

        return attrs


class OffTopicChannelNameSerializer(ModelSerializer):
    class Meta:
        model = OffTopicChannelName
        fields = ('name',)

    def to_representation(self, obj):
        return obj.name


class SnakeFactSerializer(ModelSerializer):
    class Meta:
        model = SnakeFact
        fields = ('fact',)


class SnakeIdiomSerializer(ModelSerializer):
    class Meta:
        model = SnakeIdiom
        fields = ('idiom',)


class SnakeNameSerializer(ModelSerializer):
    class Meta:
        model = SnakeName
        fields = ('name', 'scientific')


class SpecialSnakeSerializer(ModelSerializer):
    class Meta:
        model = SpecialSnake
        fields = ('name', 'images', 'info')


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'colour', 'permissions')


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title', 'embed')


class UserSerializer(BulkSerializerMixin, ModelSerializer):
    roles = PrimaryKeyRelatedField(many=True, queryset=Role.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('id', 'avatar_hash', 'name', 'discriminator', 'roles', 'in_guild')
        depth = 1
