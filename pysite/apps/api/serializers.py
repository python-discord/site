from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_bulk import BulkSerializerMixin

from .models import (
    BotSetting, DeletedMessage,
    DocumentationLink, Infraction,
    MessageDeletionContext, Nomination,
    OffTopicChannelName, Reminder,
    Role, SnakeFact,
    SnakeIdiom, SnakeName,
    SpecialSnake, Tag,
    User
)


class BotSettingSerializer(ModelSerializer):
    class Meta:
        model = BotSetting
        fields = ('name', 'data')


class DeletedMessageSerializer(ModelSerializer):
    author = PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    deletion_context = PrimaryKeyRelatedField(
        queryset=MessageDeletionContext.objects.all(),
        # This will be overriden in the `create` function
        # of the deletion context serializer.
        required=False
    )

    class Meta:
        model = DeletedMessage
        fields = (
            'id', 'author',
            'channel_id', 'content',
            'embeds', 'deletion_context'
        )


class MessageDeletionContextSerializer(ModelSerializer):
    deletedmessage_set = DeletedMessageSerializer(many=True)

    class Meta:
        model = MessageDeletionContext
        fields = ('actor', 'creation', 'id', 'deletedmessage_set')
        depth = 1

    def create(self, validated_data):
        messages = validated_data.pop('deletedmessage_set')
        deletion_context = MessageDeletionContext.objects.create(**validated_data)
        for message in messages:
            DeletedMessage.objects.create(
                deletion_context=deletion_context,
                **message
            )

        return deletion_context


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


class ExpandedInfractionSerializer(InfractionSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)

        user = User.objects.get(id=ret['user'])
        user_data = UserSerializer(user).data
        ret['user'] = user_data

        actor = User.objects.get(id=ret['actor'])
        actor_data = UserSerializer(actor).data
        ret['actor'] = actor_data

        return ret


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


class ReminderSerializer(ModelSerializer):
    author = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Reminder
        fields = ('active', 'author', 'channel_id', 'content', 'expiration', 'id')


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


class NominationSerializer(ModelSerializer):
    author = PrimaryKeyRelatedField(queryset=User.objects.all())
    user = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Nomination
        fields = ('active', 'author', 'reason', 'user', 'inserted_at')
        depth = 1
