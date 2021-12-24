"""Converters from Django models to data interchange formats and back."""
from django.db.models.query import QuerySet
from django.db.utils import IntegrityError
from rest_framework.exceptions import NotFound
from rest_framework.serializers import (
    IntegerField,
    ListSerializer,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ValidationError
)
from rest_framework.settings import api_settings
from rest_framework.validators import UniqueTogetherValidator

from .models import (  # noqa: I101 - Preserving the filter order
    BotSetting,
    DeletedMessage,
    DocumentationLink,
    Infraction,
    FilterList,
    Filter,
    MessageDeletionContext,
    Nomination,
    NominationEntry,
    OffTopicChannelName,
    OffensiveMessage,
    Reminder,
    Role,
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


ALWAYS_OPTIONAL_SETTINGS = (
    'dm_content',
    'infraction_type',
    'infraction_reason',
    'infraction_duration',
)

REQUIRED_FOR_FILTER_LIST_SETTINGS = (
    'ping_type',
    'filter_dm',
    'dm_ping_type',
    'delete_messages',
    'bypass_roles',
    'enabled',
    'enabled_channels',
    'disabled_channels',
    'disabled_categories',
)

# Required fields for custom JSON representation purposes
BASE_FILTER_FIELDS = ('id', 'content', 'description', 'additional_field')
BASE_FILTERLIST_FIELDS = ('id', 'name', 'list_type')
BASE_SETTINGS_FIELDS = (
    "bypass_roles",
    "filter_dm",
    "enabled",
    "delete_messages",
    "send_alert"
)
INFRACTION_FIELDS = ("infraction_type", "infraction_reason", "infraction_duration", "dm_content")
CHANNEL_SCOPE_FIELDS = (
    "disabled_channels",
    "disabled_categories",
    "enabled_channels",
)
SERVER_MESSAGE_FIELDS = ("server_message_text", "server_message_embed")
MENTIONS_FIELDS = ("ping_type", "dm_ping_type")

SETTINGS_FIELDS = ALWAYS_OPTIONAL_SETTINGS + REQUIRED_FOR_FILTER_LIST_SETTINGS


class FilterSerializer(ModelSerializer):
    """A class providing (de-)serialization of `Filter` instances."""

    def validate(self, data: dict) -> dict:
        """Perform infraction data + allow and disallowed lists validation."""
        if (
            data.get('infraction_reason') or data.get('infraction_duration')
        ) and not data.get('infraction_type'):
            raise ValidationError("Infraction type is required with infraction duration or reason")

        if (
            data.get('disabled_channels') is not None
            and data.get('enabled_channels') is not None
        ):
            channels_collection = data['disabled_channels'] + data['enabled_channels']
            if len(channels_collection) != len(set(channels_collection)):
                raise ValidationError("Enabled and Disabled channels lists contain duplicates.")

        if data.get('disabled_categories') is not None:
            categories_collection = data['disabled_categories']
            if len(categories_collection) != len(set(categories_collection)):
                raise ValidationError("Disabled categories lists contain duplicates.")

        return data

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = Filter
        fields = (
            'id', 'content', 'description', 'additional_field', 'filter_list'
        ) + SETTINGS_FIELDS
        extra_kwargs = {
            field: {'required': False, 'allow_null': True} for field in SETTINGS_FIELDS
        } | {
            'infraction_reason': {'allow_blank': True, 'allow_null': True, 'required': False},
            'enabled_channels': {'allow_empty': True, 'allow_null': True, 'required': False},
            'disabled_channels': {'allow_empty': True, 'allow_null': True, 'required': False},
            'disabled_categories': {'allow_empty': True, 'allow_null': True, 'required': False},
        }

    def to_representation(self, instance: Filter) -> dict:
        """
        Provides a custom JSON representation to the Filter Serializers.

        This representation restructures how the Filter is represented.
        It groups the Infraction, Channel and Mention related fields into their own separated group.

        Furthermore, it puts the fields that meant to represent Filter settings,
        into a sub-field called `settings`.
        """
        schema_settings = {
            "settings":
                {name: getattr(instance, name) for name in BASE_SETTINGS_FIELDS}
                | {"infraction": {name: getattr(instance, name) for name in INFRACTION_FIELDS}}
                | {
                    "channel_scope":
                        {name: getattr(instance, name) for name in CHANNEL_SCOPE_FIELDS}
                } | {
                    "mentions":
                        {
                            schema_field_name: getattr(instance, schema_field_name)
                            for schema_field_name in MENTIONS_FIELDS
                        }
                }
        } | {
            "server_message":
            {
                schema_field_name: getattr(instance, schema_field_name)
                for schema_field_name in SERVER_MESSAGE_FIELDS
            }
        }
        schema_base = {name: getattr(instance, name) for name in BASE_FILTER_FIELDS} | \
                      {"filter_list": instance.filter_list.id}

        return schema_base | schema_settings


class FilterListSerializer(ModelSerializer):
    """A class providing (de-)serialization of `FilterList` instances."""

    filters = FilterSerializer(many=True, read_only=True)

    def validate(self, data: dict) -> dict:
        """Perform infraction data + allow and disallowed lists validation."""
        if (
            data.get('infraction_reason') or data.get('infraction_duration')
        ) and not data.get('infraction_type'):
            raise ValidationError("Infraction type is required with infraction duration or reason")

        if (
            data.get('disabled_channels') is not None
            and data.get('enabled_channels') is not None
        ):
            channels_collection = data['disabled_channels'] + data['enabled_channels']
            if len(channels_collection) != len(set(channels_collection)):
                raise ValidationError("Enabled and Disabled channels lists contain duplicates.")

        if data.get('disabled_categories') is not None:
            categories_collection = data['disabled_categories']
            if len(categories_collection) != len(set(categories_collection)):
                raise ValidationError("Disabled categories lists contain duplicates.")

        return data

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = FilterList
        fields = ('id', 'name', 'list_type', 'filters') + SETTINGS_FIELDS
        extra_kwargs = {
            field: {'required': False, 'allow_null': True} for field in ALWAYS_OPTIONAL_SETTINGS
        } | {
            'infraction_reason': {'allow_blank': True, 'allow_null': True, 'required': False},
            'enabled_channels': {'allow_empty': True},
            'disabled_channels': {'allow_empty': True},
            'disabled_categories': {'allow_empty': True},
        }

        # Ensure that we can only have one filter list with the same name and field
        validators = [
            UniqueTogetherValidator(
                queryset=FilterList.objects.all(),
                fields=('name', 'list_type'),
                message=(
                    "A filterlist with the same name and type already exist."
                )
            ),
        ]

    def to_representation(self, instance: FilterList) -> dict:
        """
        Provides a custom JSON representation to the FilterList Serializers.

        This representation restructures how the Filter is represented.
        It groups the Infraction, Channel and Mention related fields into their own separated group.

        Furthermore, it puts the fields that meant to represent FilterList settings,
        into a sub-field called `settings`.
        """
        # Fetches the relating filters
        filters = [
            FilterSerializer(many=False).to_representation(
                instance=item
            ) for item in Filter.objects.filter(
                filter_list=instance.id
            )
        ]
        schema_base = {name: getattr(instance, name) for name in BASE_FILTERLIST_FIELDS} \
            | {"filters": filters}
        schema_settings_base = {name: getattr(instance, name) for name in BASE_SETTINGS_FIELDS}
        schema_settings_categories = {
            "infraction":
            {name: getattr(instance, name) for name in INFRACTION_FIELDS}} \
            | {
            "channel_scope":
            {name: getattr(instance, name) for name in CHANNEL_SCOPE_FIELDS}} | {
            "mentions": {
                schema_field_name: getattr(instance, schema_field_name)
                for schema_field_name in MENTIONS_FIELDS
            }
        } | {
            "server_message": {
                schema_field_name: getattr(instance, schema_field_name)
                for schema_field_name in SERVER_MESSAGE_FIELDS
            }
        }
        return schema_base | {"settings": schema_settings_base | schema_settings_categories}


class InfractionSerializer(ModelSerializer):
    """A class providing (de-)serialization of `Infraction` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = Infraction
        fields = (
            'id',
            'inserted_at',
            'expires_at',
            'active',
            'user',
            'actor',
            'type',
            'reason',
            'hidden',
            'dm_sent'
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
        if hidden and infr_type in ('superstar', 'warning', 'voice_ban'):
            raise ValidationError({'hidden': [f'{infr_type} infractions cannot be hidden.']})

        if not hidden and infr_type in ('note',):
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
            'active',
            'author',
            'jump_url',
            'channel_id',
            'content',
            'expiration',
            'id',
            'mentions',
            'failures'
        )


class RoleSerializer(ModelSerializer):
    """A class providing (de-)serialization of `Role` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = Role
        fields = ('id', 'name', 'colour', 'permissions', 'position')


class UserListSerializer(ListSerializer):
    """List serializer for User model to handle bulk updates."""

    def create(self, validated_data: list) -> list:
        """Override create method to optimize django queries."""
        new_users = []
        seen = set()

        for user_dict in validated_data:
            if user_dict["id"] in seen:
                raise ValidationError(
                    {"id": [f"User with ID {user_dict['id']} given multiple times."]}
                )
            seen.add(user_dict["id"])
            new_users.append(User(**user_dict))

        User.objects.bulk_create(new_users, ignore_conflicts=True)
        return []

    def update(self, queryset: QuerySet, validated_data: list) -> list:
        """
        Override update method to support bulk updates.

        ref:https://www.django-rest-framework.org/api-guide/serializers/#customizing-multiple-update
        """
        object_ids = set()

        for data in validated_data:
            try:
                if data["id"] in object_ids:
                    # If request data contains users with same ID.
                    raise ValidationError(
                        {"id": [f"User with ID {data['id']} given multiple times."]}
                    )
            except KeyError:
                # If user ID not provided in request body.
                raise ValidationError(
                    {"id": ["This field is required."]}
                )
            object_ids.add(data["id"])

        # filter queryset
        filtered_instances = queryset.filter(id__in=object_ids)

        instance_mapping = {user.id: user for user in filtered_instances}

        updated = []
        fields_to_update = set()
        for user_data in validated_data:
            for key in user_data:
                fields_to_update.add(key)

                try:
                    user = instance_mapping[user_data["id"]]
                except KeyError:
                    raise NotFound({"detail": f"User with id {user_data['id']} not found."})

                user.__dict__.update(user_data)
            updated.append(user)

        fields_to_update.remove("id")

        if not fields_to_update:
            # Raise ValidationError when only id field is given.
            raise ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: ["Insufficient data provided."]}
            )

        User.objects.bulk_update(updated, fields_to_update)
        return updated


class UserSerializer(ModelSerializer):
    """A class providing (de-)serialization of `User` instances."""

    # ID field must be explicitly set as the default id field is read-only.
    id = IntegerField(min_value=0)

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = User
        fields = ('id', 'name', 'discriminator', 'roles', 'in_guild')
        depth = 1
        list_serializer_class = UserListSerializer

    def create(self, validated_data: dict) -> User:
        """Override create method to catch IntegrityError."""
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError({"id": ["User with ID already present."]})


class NominationEntrySerializer(ModelSerializer):
    """A class providing (de-)serialization of `NominationEntry` instances."""

    # We need to define it here, because we don't want that nomination ID
    # return inside nomination response entry, because ID is already available
    # as top-level field. Queryset is required if field is not read only.
    nomination = PrimaryKeyRelatedField(
        queryset=Nomination.objects.all(),
        write_only=True
    )

    class Meta:
        """Metadata defined for the Django REST framework."""

        model = NominationEntry
        fields = ('nomination', 'actor', 'reason', 'inserted_at')


class NominationSerializer(ModelSerializer):
    """A class providing (de-)serialization of `Nomination` instances."""

    entries = NominationEntrySerializer(many=True, read_only=True)

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = Nomination
        fields = (
            'id', 'active', 'user', 'inserted_at', 'end_reason', 'ended_at', 'reviewed', 'entries'
        )


class OffensiveMessageSerializer(ModelSerializer):
    """A class providing (de-)serialization of `OffensiveMessage` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = OffensiveMessage
        fields = ('id', 'channel_id', 'delete_date')
