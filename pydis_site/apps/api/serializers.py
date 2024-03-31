"""Converters from Django models to data interchange formats and back."""
from datetime import timedelta
from typing import Any

from django.db import models
from django.db.models.query import QuerySet
from django.db.utils import IntegrityError
from rest_framework.exceptions import NotFound
from rest_framework.serializers import (
    BooleanField,
    CharField,
    ChoiceField,
    DateTimeField,
    DurationField,
    IntegerField,
    JSONField,
    ListField,
    ListSerializer,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ValidationError
)
from rest_framework.settings import api_settings
from rest_framework.validators import UniqueTogetherValidator

from .models import (
    AocAccountLink,
    AocCompletionistBlock,
    BotSetting,
    BumpedThread,
    DeletedMessage,
    DocumentationLink,
    Filter,
    FilterList,
    Infraction,
    MailingList,
    MailingListSeenItem,
    MessageDeletionContext,
    Nomination,
    NominationEntry,
    OffTopicChannelName,
    OffensiveMessage,
    Reminder,
    Role,
    User
)

class FrozenFieldsMixin:
    """
    Serializer mixin that allows adding non-updateable fields to a serializer.

    To use, inherit from the mixin and specify the fields that should only be
    written to on creation in the `frozen_fields` attribute of the `Meta` class
    in a serializer.

    See also the DRF discussion for this feature at
    https://github.com/encode/django-rest-framework/discussions/8606, which may
    eventually provide an official way to implement this.
    """

    def update(self, instance: models.Model, validated_data: dict) -> models.Model:
        """Validate that no frozen fields were changed and update the instance."""
        for field_name in getattr(self.Meta, 'frozen_fields', ()):
            if field_name in validated_data:
                raise ValidationError(
                    {
                        field_name: ["This field cannot be updated."]
                    }
                )
        return super().update(instance, validated_data)


class BotSettingSerializer(ModelSerializer):
    """A class providing (de-)serialization of `BotSetting` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = BotSetting
        fields = ('name', 'data')


class ListBumpedThreadSerializer(ListSerializer):
    """Custom ListSerializer to override to_representation() when list views are triggered."""

    def to_representation(self, objects: list[BumpedThread]) -> int:
        """
        Used by the `ListModelMixin` to return just the list of bumped thread ids.

        Only the thread_id field is useful, hence it is unnecessary to create a nested dictionary.

        Additionally, this allows bumped thread routes to simply return an
        array of thread_id ints instead of objects, saving on bandwidth.
        """
        return [obj.thread_id for obj in objects]


class BumpedThreadSerializer(ModelSerializer):
    """A class providing (de-)serialization of `BumpedThread` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        list_serializer_class = ListBumpedThreadSerializer
        model = BumpedThread
        fields = ('thread_id',)


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
        DeletedMessage.objects.bulk_create(
            DeletedMessage(deletion_context=deletion_context, **message) for message in messages
        )
        return deletion_context


class DocumentationLinkSerializer(ModelSerializer):
    """A class providing (de-)serialization of `DocumentationLink` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = DocumentationLink
        fields = ('package', 'base_url', 'inventory_url')


#  region: filters serializers

SETTINGS_FIELDS = (
    'dm_content',
    'dm_embed',
    'infraction_type',
    'infraction_reason',
    'infraction_duration',
    'infraction_channel',
    'guild_pings',
    'filter_dm',
    'dm_pings',
    'remove_context',
    'send_alert',
    'bypass_roles',
    'enabled',
    'enabled_channels',
    'disabled_channels',
    'enabled_categories',
    'disabled_categories',
)

ALLOW_BLANK_SETTINGS = (
    'dm_content',
    'dm_embed',
    'infraction_reason',
)

ALLOW_EMPTY_SETTINGS = (
    'enabled_channels',
    'disabled_channels',
    'enabled_categories',
    'disabled_categories',
    'guild_pings',
    'dm_pings',
    'bypass_roles',
)

# Required fields for custom JSON representation purposes
BASE_FILTER_FIELDS = (
    'id', 'created_at', 'updated_at', 'content', 'description', 'additional_settings'
)
BASE_FILTERLIST_FIELDS = ('id', 'created_at', 'updated_at', 'name', 'list_type')
BASE_SETTINGS_FIELDS = (
    'bypass_roles',
    'filter_dm',
    'enabled',
    'remove_context',
    'send_alert'
)
INFRACTION_AND_NOTIFICATION_FIELDS = (
    'infraction_type',
    'infraction_reason',
    'infraction_duration',
    'infraction_channel',
    'dm_content',
    'dm_embed'
)
CHANNEL_SCOPE_FIELDS = (
    'disabled_channels',
    'disabled_categories',
    'enabled_channels',
    'enabled_categories'
)
MENTIONS_FIELDS = ('guild_pings', 'dm_pings')

MAX_TIMEOUT_DURATION = timedelta(days=28)


def _create_meta_extra_kwargs(*, for_filter: bool) -> dict[str, dict[str, bool]]:
    """Create the extra kwargs for the Meta classes of the Filter and FilterList serializers."""
    extra_kwargs = {}
    for field in SETTINGS_FIELDS:
        field_args = {'required': False, 'allow_null': True} if for_filter else {}
        if field in ALLOW_BLANK_SETTINGS:
            field_args['allow_blank'] = True
        if field in ALLOW_EMPTY_SETTINGS:
            field_args['allow_empty'] = True
        extra_kwargs[field] = field_args
    return extra_kwargs


def get_field_value(data: dict, field_name: str) -> Any:
    """Get the value directly from the key, or from the filter list if it's missing or is None."""
    if data.get(field_name) is not None:
        return data[field_name]
    return getattr(data['filter_list'], field_name)


class FilterSerializer(ModelSerializer):
    """A class providing (de-)serialization of `Filter` instances."""

    # Remove the following once this regression from DRF 3.15 is fixed:
    # https://github.com/encode/django-rest-framework/issues/9345
    # ------------------------------8<----------------------------------
    id = IntegerField(label='ID', read_only=True)
    created_at = DateTimeField(read_only=True)
    updated_at = DateTimeField(read_only=True)
    content = CharField(
        help_text='The definition of this filter.',
        style={'base_template': 'textarea.html'},
    )
    description = CharField(
        allow_null=True,
        help_text='Why this filter has been added.',
        required=False,
        style={'base_template': 'textarea.html'}
    )
    additional_settings = JSONField(
        decoder=None,
        encoder=None,
        help_text='Additional settings which are specific to this filter.',
        required=False,
        style={'base_template': 'textarea.html'},
    )
    filter_list = PrimaryKeyRelatedField(
        help_text='The filter list containing this filter.',
        queryset=FilterList.objects.all(),
    )
    dm_content = CharField(
        allow_blank=True,
        allow_null=True,
        help_text='The DM to send to a user triggering this filter.',
        max_length=1000,
        required=False,
    )
    dm_embed = CharField(
        allow_blank=True,
        allow_null=True,
        help_text='The content of the DM embed',
        max_length=2000,
        required=False,
    )
    infraction_type = ChoiceField(
        allow_null=True,
        choices=[('NONE', 'None'), ('NOTE', 'Note'), ('WARNING', 'Warning'),
                 ('WATCH', 'Watch'), ('TIMEOUT', 'Timeout'), ('KICK', 'Kick'),
                 ('BAN', 'Ban'), ('SUPERSTAR', 'Superstar'), ('VOICE_BAN', 'Voice Ban'),
                 ('VOICE_MUTE', 'Voice Mute')],
        help_text='The infraction to apply to this user.',
        required=False,
    )
    infraction_reason = CharField(
        allow_blank=True,
        allow_null=True,
        help_text='The reason to give for the infraction.',
        max_length=1000,
        required=False,
    )
    infraction_duration = DurationField(
        allow_null=True,
        help_text='The duration of the infraction. 0 for permanent.',
        required=False,
    )
    infraction_channel = IntegerField(
        allow_null=True,
        help_text='Channel in which to send the infraction.',
        max_value=9223372036854775807,
        min_value=0,
        required=False,
    )
    guild_pings = ListField(
        allow_empty=True,
        allow_null=True,
        child=CharField(label='Guild pings', max_length=100),
        help_text='Who to ping when this filter triggers.',
        required=False,
    )
    filter_dm = BooleanField(
        allow_null=True,
        help_text='Whether DMs should be filtered.',
        required=False,
    )
    dm_pings = ListField(
        allow_empty=True,
        allow_null=True,
        child=CharField(label='Dm pings', max_length=100),
        help_text='Who to ping when this filter triggers on a DM.',
        required=False,
    )
    remove_context = BooleanField(
        allow_null=True,
        help_text='Whether this filter should remove the context (such as a message) triggering it.',
        required=False,
    )
    send_alert = BooleanField(
        allow_null=True,
        help_text='Whether an alert should be sent.',
        required=False,
    )
    bypass_roles = ListField(
        allow_empty=True,
        allow_null=True,
        child=CharField(label='Bypass roles', max_length=100),
        help_text='Roles and users who can bypass this filter.',
        required=False,
    )
    enabled = BooleanField(
        allow_null=True,
        help_text='Whether this filter is currently enabled.',
        required=False,
    )
    enabled_channels = ListField(
        allow_empty=True,
        allow_null=True,
        child=CharField(label='Enabled channels', max_length=100),
        help_text="Channels in which to run the filter even if it's disabled in the category.",
        required=False,
    )
    disabled_channels = ListField(
        allow_empty=True,
        allow_null=True,
        child=CharField(label='Disabled channels', max_length=100),
        help_text="Channels in which to not run the filter even if it's enabled in the category.",
        required=False,
    )
    enabled_categories = ListField(
        allow_empty=True,
        allow_null=True,
        child=CharField(label='Enabled categories', max_length=100),
        help_text='The only categories in which to run the filter.',
        required=False,
    )
    disabled_categories = ListField(
        allow_empty=True, allow_null=True,
        child=CharField(label='Disabled categories', max_length=100),
        help_text='Categories in which to not run the filter.',
        required=False,
    )
    # ------------------------------8<----------------------------------

    def validate(self, data: dict) -> dict:
        """Perform infraction data + allowed and disallowed lists validation."""
        infraction_type = get_field_value(data, 'infraction_type')
        infraction_duration = get_field_value(data, 'infraction_duration')
        if (
            (get_field_value(data, 'infraction_reason') or infraction_duration)
            and infraction_type == 'NONE'
        ):
            raise ValidationError(
                "Infraction type is required with infraction duration or reason."
            )

        if (
            infraction_type == 'TIMEOUT'
            and (not infraction_duration or infraction_duration > MAX_TIMEOUT_DURATION)
        ):
            raise ValidationError(
                f"A timeout cannot be longer than {MAX_TIMEOUT_DURATION.days} days."
            )

        common_channels = (
            set(get_field_value(data, 'disabled_channels'))
            & set(get_field_value(data, 'enabled_channels'))
        )
        if common_channels:
            raise ValidationError(
                "You can't have the same value in both enabled and disabled channels lists:"
                f" {', '.join(repr(channel) for channel in common_channels)}."
            )

        common_categories = (
            set(get_field_value(data, 'disabled_categories'))
            & set(get_field_value(data, 'enabled_categories'))
        )
        if common_categories:
            raise ValidationError(
                "You can't have the same value in both enabled and disabled categories lists:"
                f" {', '.join(repr(category) for category in common_categories)}."
            )

        return data

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = Filter
        fields = (
            'id',
            'created_at',
            'updated_at',
            'content',
            'description',
            'additional_settings',
            'filter_list'
        ) + SETTINGS_FIELDS
        extra_kwargs = _create_meta_extra_kwargs(for_filter=True)

    def create(self, validated_data: dict) -> User:
        """Override the create method to catch violations of the custom uniqueness constraint."""
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError(
                "Check if a filter with this combination of content "
                "and settings already exists in this filter list."
            )

    def to_representation(self, instance: Filter) -> dict:
        """
        Provides a custom JSON representation to the Filter Serializers.

        This representation restructures how the Filter is represented.
        It groups the Infraction, Channel and Mention related fields into their own separated group.

        Furthermore, it puts the fields that meant to represent Filter settings,
        into a sub-field called `settings`.
        """
        settings = {name: getattr(instance, name) for name in BASE_SETTINGS_FIELDS}
        settings['infraction_and_notification'] = {
            name: getattr(instance, name) for name in INFRACTION_AND_NOTIFICATION_FIELDS
        }
        settings['channel_scope'] = {
            name: getattr(instance, name) for name in CHANNEL_SCOPE_FIELDS
        }
        settings['mentions'] = {
            name: getattr(instance, name) for name in MENTIONS_FIELDS
        }

        schema = {name: getattr(instance, name) for name in BASE_FILTER_FIELDS}
        schema['filter_list'] = instance.filter_list.id
        schema['settings'] = settings
        return schema


class FilterListSerializer(ModelSerializer):
    """A class providing (de-)serialization of `FilterList` instances."""

    filters = FilterSerializer(many=True, read_only=True)

    def validate(self, data: dict) -> dict:
        """Perform infraction data + allow and disallowed lists validation."""
        infraction_duration = data.get('infraction_duration')
        if (
            data.get('infraction_reason') or infraction_duration
        ) and not data.get('infraction_type'):
            raise ValidationError("Infraction type is required with infraction duration or reason")

        if (
            data.get('disabled_channels') is not None
            and data.get('enabled_channels') is not None
        ):
            common_channels = set(data['disabled_channels']) & set(data['enabled_channels'])
            if common_channels:
                raise ValidationError(
                    "You can't have the same value in both enabled and disabled channels lists:"
                    f" {', '.join(repr(channel) for channel in common_channels)}."
                )

        if (
            data.get('infraction_type') == 'TIMEOUT'
            and (not infraction_duration or infraction_duration > MAX_TIMEOUT_DURATION)
        ):
            raise ValidationError(
                f"A timeout cannot be longer than {MAX_TIMEOUT_DURATION.days} days."
            )

        if (
            data.get('disabled_categories') is not None
            and data.get('enabled_categories') is not None
        ):
            common_categories = set(data['disabled_categories']) & set(data['enabled_categories'])
            if common_categories:
                raise ValidationError(
                    "You can't have the same value in both enabled and disabled categories lists:"
                    f" {', '.join(repr(category) for category in common_categories)}."
                )

        return data

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = FilterList
        fields = (
            'id', 'created_at', 'updated_at', 'name', 'list_type', 'filters'
        ) + SETTINGS_FIELDS
        extra_kwargs = _create_meta_extra_kwargs(for_filter=False)

        # Ensure there can only be one filter list with the same name and type.
        validators = [
            UniqueTogetherValidator(
                queryset=FilterList.objects.all(),
                fields=('name', 'list_type'),
                message=(
                    "A filterlist with the same name and type already exists."
                )
            ),
        ]

    def to_representation(self, instance: FilterList) -> dict:
        """
        Provides a custom JSON representation to the FilterList Serializers.

        This representation restructures how the Filter is represented.
        It groups the Infraction, Channel, and Mention related fields
        into their own separated groups.

        Furthermore, it puts the fields that are meant to represent FilterList settings,
        into a sub-field called `settings`.
        """
        schema = {name: getattr(instance, name) for name in BASE_FILTERLIST_FIELDS}
        schema['filters'] = [
            FilterSerializer(many=False).to_representation(instance=item)
            for item in Filter.objects.filter(filter_list=instance.id)
        ]

        settings = {name: getattr(instance, name) for name in BASE_SETTINGS_FIELDS}
        settings['infraction_and_notification'] = {
            name: getattr(instance, name) for name in INFRACTION_AND_NOTIFICATION_FIELDS
        }
        settings['channel_scope'] = {name: getattr(instance, name) for name in CHANNEL_SCOPE_FIELDS}
        settings['mentions'] = {name: getattr(instance, name) for name in MENTIONS_FIELDS}

        schema['settings'] = settings
        return schema

#  endregion


class InfractionSerializer(FrozenFieldsMixin, ModelSerializer):
    """A class providing (de-)serialization of `Infraction` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = Infraction
        fields = (
            'id',
            'inserted_at',
            'last_applied',
            'expires_at',
            'active',
            'user',
            'actor',
            'type',
            'reason',
            'hidden',
            'dm_sent',
            'jump_url'
        )
        frozen_fields = ('id', 'inserted_at', 'type', 'user', 'actor', 'hidden')

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
        if hidden and infr_type in ('superstar', 'warning', 'voice_ban', 'voice_mute'):
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

        ret['user'] = UserSerializer(instance.user).data
        ret['actor'] = UserSerializer(instance.actor).data

        return ret


class OffTopicChannelNameListSerializer(ListSerializer):
    """Custom ListSerializer to override to_representation() when list views are triggered."""

    def to_representation(self, objects: list[OffTopicChannelName]) -> list[str]:
        """
        Return a list with all `OffTopicChannelName`s in the database.

        This returns the list of off topic channel names. We want to only return
        the name attribute, hence it is unnecessary to create a nested dictionary.
        Additionally, this allows off topic channel name routes to simply return an
        array of names instead of objects, saving on bandwidth.
        """
        return [obj.name for obj in objects]


class OffTopicChannelNameSerializer(ModelSerializer):
    """A class providing (de-)serialization of `OffTopicChannelName` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        list_serializer_class = OffTopicChannelNameListSerializer
        model = OffTopicChannelName
        fields = ('name', 'used', 'active')


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


class AocCompletionistBlockSerializer(ModelSerializer):
    """A class providing (de-)serialization of `AocCompletionistBlock` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = AocCompletionistBlock
        fields = ("user", "is_blocked", "reason")


class AocAccountLinkSerializer(ModelSerializer):
    """A class providing (de-)serialization of `AocAccountLink` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = AocAccountLink
        fields = ("user", "aoc_username")


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


class NominationSerializer(FrozenFieldsMixin, ModelSerializer):
    """A class providing (de-)serialization of `Nomination` instances."""

    entries = NominationEntrySerializer(many=True, read_only=True)

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = Nomination
        fields = (
            'id',
            'active',
            'user',
            'inserted_at',
            'end_reason',
            'ended_at',
            'reviewed',
            'entries',
            'thread_id'
        )
        frozen_fields = ('id', 'inserted_at', 'user', 'ended_at')


class OffensiveMessageSerializer(FrozenFieldsMixin, ModelSerializer):
    """A class providing (de-)serialization of `OffensiveMessage` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = OffensiveMessage
        fields = ('id', 'channel_id', 'delete_date')
        frozen_fields = ('id', 'channel_id')


class MailingListSeenItemListSerializer(ListSerializer):
    """A class providing (de-)serialization of `MailingListSeenItem` instances as a list."""

    def to_representation(self, objects: list[MailingListSeenItem]) -> list[str]:
        """Return the hashes of each seen mailing list item."""
        return [obj['hash'] for obj in objects.values('hash')]


class MailingListSeenItemSerializer(ModelSerializer):
    """A class providing (de-)serialization of `MailingListSeenItem` instances."""

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = MailingListSeenItem
        # Since this is only exposed on the parent mailing list model,
        # we don't need information about the list or even the ID.
        fields = ('hash',)
        list_serializer_class = MailingListSeenItemListSerializer


class MailingListSerializer(FrozenFieldsMixin, ModelSerializer):
    """A class providing (de-)serialization of `MailingList` instances."""

    seen_items = MailingListSeenItemSerializer(many=True, required=False)

    class Meta:
        """Metadata defined for the Django REST Framework."""

        model = MailingList
        fields = ('id', 'name', 'seen_items')
        frozen_fields = ('name',)
