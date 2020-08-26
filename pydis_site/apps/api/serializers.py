"""Converters from Django models to data interchange formats and back."""
from django.db.models.query import QuerySet
from rest_framework.serializers import (
    ListSerializer,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ValidationError
)
from rest_framework.settings import api_settings
from rest_framework.utils import html
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_bulk import BulkSerializerMixin

from .models import (
    BotSetting,
    DeletedMessage,
    DocumentationLink,
    FilterList,
    Infraction,
    LogEntry,
    MessageDeletionContext,
    Nomination,
    OffTopicChannelName,
    OffensiveMessage,
    Reminder,
    Role,
    Tag,
    User
)


class BotSettingSerializer(ModelSerializer):
    """A class providing (de-)serialization of `BotSetting` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = BotSetting
        fields = ('name', 'data')


class DeletedMessageSerializer(ModelSerializer):
    """
    A class providing (de-)serialization of `DeletedMessage` instances.

    The serializer generally requires a valid `deletion_context` to be
    given, which should be created beforehand. See the `DeletedMessage`
    model for more information.
    """

    author = PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    deletion_context = PrimaryKeyRelatedField(
        queryset=MessageDeletionContext.objects.all(),
        # This will be overridden in the `create` function
        # of the deletion context serializer.
        required=False
    )

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = DeletedMessage
        fields = (
            'id', 'author',
            'channel_id', 'content',
            'embeds', 'deletion_context',
            'attachments'
        )


class MessageDeletionContextSerializer(ModelSerializer):
    """A class providing (de-)serialization of `MessageDeletionContext` instances."""

    actor = PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    deletedmessage_set = DeletedMessageSerializer(many=True)

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = MessageDeletionContext
        fields = ('actor', 'creation', 'id', 'deletedmessage_set')
        depth = 1

    def create(self, validated_data: dict) -> MessageDeletionContext:
        """
        Return a `MessageDeletionContext` based on the given data.

        In addition to the normal attributes expected by the `MessageDeletionContext` model
        itself, this serializer also allows for passing the `deletedmessage_set` element
        which contains messages that were deleted as part of this context.
        """
        messages = validated_data.pop('deletedmessage_set')
        deletion_context = MessageDeletionContext.objects.create(**validated_data)
        for message in messages:
            DeletedMessage.objects.create(
                deletion_context=deletion_context,
                **message
            )

        return deletion_context


class DocumentationLinkSerializer(ModelSerializer):
    """A class providing (de-)serialization of `DocumentationLink` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = DocumentationLink
        fields = ('package', 'base_url', 'inventory_url')


class FilterListSerializer(ModelSerializer):
    """A class providing (de-)serialization of `FilterList` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = FilterList
        fields = ('id', 'created_at', 'updated_at', 'type', 'allowed', 'content', 'comment')

        # This validator ensures only one filterlist with the
        # same content can exist. This means that we cannot have both an allow
        # and a deny for the same item, and we cannot have duplicates of the
        # same item.
        validators = [
            UniqueTogetherValidator(
                queryset=FilterList.objects.all(),
                fields=['content', 'type'],
                message=(
                    "A filterlist for this item already exists. "
                    "Please note that you cannot add the same item to both allow and deny."
                )
            ),
        ]


class InfractionSerializer(ModelSerializer):
    """A class providing (de-)serialization of `Infraction` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = Infraction
        fields = (
            'id', 'inserted_at', 'expires_at', 'active', 'user', 'actor', 'type', 'reason', 'hidden'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Infraction.objects.filter(active=True),
                fields=['user', 'type', 'active'],
                message='This user already has an active infraction of this type.',
            )
        ]

    def validate(self, attrs: dict) -> dict:
        """Validate data constraints for the given data and abort if it is invalid."""
        infr_type = attrs.get('type')

        active = attrs.get('active')
        if active and infr_type in ('note', 'warning', 'kick'):
            raise ValidationError({'active': [f'{infr_type} infractions cannot be active.']})

        expires_at = attrs.get('expires_at')
        if expires_at and infr_type in ('kick', 'warning'):
            raise ValidationError({'expires_at': [f'{infr_type} infractions cannot expire.']})

        hidden = attrs.get('hidden')
        if hidden and infr_type in ('superstar', 'warning'):
            raise ValidationError({'hidden': [f'{infr_type} infractions cannot be hidden.']})

        if not hidden and infr_type in ('note', ):
            raise ValidationError({'hidden': [f'{infr_type} infractions must be hidden.']})

        return attrs


class ExpandedInfractionSerializer(InfractionSerializer):
    """
    A class providing expanded (de-)serialization of `Infraction` instances.

    In addition to the fields of `Infraction` objects themselves, this
    serializer also attaches the `user` and `actor` fields when serializing.
    """

    def to_representation(self, instance: Infraction) -> dict:
        """Return the dictionary representation of this infraction."""
        ret = super().to_representation(instance)

        user = User.objects.get(id=ret['user'])
        user_data = UserSerializer(user).data
        ret['user'] = user_data

        actor = User.objects.get(id=ret['actor'])
        actor_data = UserSerializer(actor).data
        ret['actor'] = actor_data

        return ret


class LogEntrySerializer(ModelSerializer):
    """A class providing (de-)serialization of `LogEntry` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = LogEntry
        fields = (
            'application', 'logger_name', 'timestamp',
            'level', 'module', 'line', 'message'
        )


class OffTopicChannelNameSerializer(ModelSerializer):
    """A class providing (de-)serialization of `OffTopicChannelName` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = OffTopicChannelName
        fields = ('name',)

    def to_representation(self, obj: OffTopicChannelName) -> str:
        """
        Return the representation of this `OffTopicChannelName`.

        This only returns the name of the off topic channel name. As the model
        only has a single attribute, it is unnecessary to create a nested dictionary.
        Additionally, this allows off topic channel name routes to simply return an
        array of names instead of objects, saving on bandwidth.
        """
        return obj.name


class ReminderSerializer(ModelSerializer):
    """A class providing (de-)serialization of `Reminder` instances."""

    author = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = Reminder
        fields = (
            'active', 'author', 'jump_url', 'channel_id', 'content', 'expiration', 'id', 'mentions'
        )


class RoleSerializer(ModelSerializer):
    """A class providing (de-)serialization of `Role` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = Role
        fields = ('id', 'name', 'colour', 'permissions', 'position')


class TagSerializer(ModelSerializer):
    """A class providing (de-)serialization of `Tag` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = Tag
        fields = ('title', 'embed')


class UserListSerializer(ListSerializer):
    """List serializer for User model to handle bulk updates."""

    def to_internal_value(self, data: list) -> list:
        """
        Overriding `to_internal_value` function with a few changes to support bulk updates.

        ref: https://github.com/miki725/django-rest-framework-bulk/issues/68

        List of dicts of native values <- List of dicts of primitive datatypes.
        """
        if html.is_html_input(data):
            data = html.parse_html_list(data, default=[])

        if not isinstance(data, list):
            message = self.error_messages['not_a_list'].format(
                input_type=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='not_a_list')

        if not self.allow_empty and len(data) == 0:
            message = self.error_messages['empty']
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='empty')

        ret = []
        errors = []

        for item in data:
            # inserted code
            # -----------------
            try:
                self.child.instance = self.instance.get(id=item['id'])
            except (User.DoesNotExist, AttributeError):
                self.child.instance = None
            # -----------------
            self.child.initial_data = item
            try:
                validated = self.child.run_validation(item)
            except ValidationError as exc:
                errors.append(exc.detail)
            else:
                ret.append(validated)
                errors.append({})

        if any(errors):
            raise ValidationError(errors)

        return ret

    def update(self, instance: QuerySet, validated_data: list) -> list:
        """
        Override update method to support bulk updates.

        ref:https://www.django-rest-framework.org/api-guide/serializers/#customizing-multiple-update
        """
        instance_mapping = {user.id: user for user in instance}
        data_mapping = {item['id']: item for item in validated_data}

        updated = []
        for book_id, data in data_mapping.items():
            book = instance_mapping.get(book_id, None)
            if book is not None:
                updated.append(self.child.update(book, data))

        return updated


class UserSerializer(BulkSerializerMixin, ModelSerializer):
    """A class providing (de-)serialization of `User` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = User
        fields = ('id', 'name', 'discriminator', 'roles', 'in_guild')
        depth = 1
        list_serializer_class = UserListSerializer


class NominationSerializer(ModelSerializer):
    """A class providing (de-)serialization of `Nomination` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = Nomination
        fields = (
            'id', 'active', 'actor', 'reason', 'user',
            'inserted_at', 'end_reason', 'ended_at')


class OffensiveMessageSerializer(ModelSerializer):
    """A class providing (de-)serialization of `OffensiveMessage` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = OffensiveMessage
        fields = ('id', 'channel_id', 'delete_date')
