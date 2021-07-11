from typing import List

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint


class FilterListType(models.IntegerChoices):
    """Choice between allow or deny for a list type."""

    ALLOW: 1
    DENY: 0


class InfractionType(models.TextChoices):
    """Possible type of infractions."""

    NOTE = "Note"
    WARN = "Warn"
    MUTE = "Mute"
    KICK = "Kick"
    BAN = "Ban"


# Valid special values in ping related fields
VALID_PINGS = ("everyone", "here", "moderators", "onduty", "admins")


def validate_ping_field(value_list: List[str]) -> None:
    """Validate that the values are either a special value or a UID."""
    for value in value_list:
        # Check if it is a special value
        if value in VALID_PINGS:
            continue
        # Check if it is a UID
        if value.isnumeric():
            continue

        raise ValidationError(f"{value!r} isn't a valid ping type.")


class FilterList(models.Model):
    """Represent a list in its allow or deny form."""

    name = models.CharField(max_length=50, help_text="The unique name of this list.")
    list_type = models.IntegerField(
        choices=FilterListType.choices,
        help_text="Whether this list is an allowlist or denylist"
    )

    filters = models.ManyToManyField("Filter", help_text="The content of this list.", default=[])
    default_settings = models.ForeignKey(
        "FilterSettings",
        models.CASCADE,
        help_text="Default parameters of this list."
    )

    class Meta:
        """Constrain name and list_type unique."""

        constraints = (
            UniqueConstraint(fields=("name", "list_type"), name="unique_name_type"),
        )

    def __str__(self) -> str:
        return f"Filter {'allow' if self.list_type == 1 else 'deny'}list {self.name!r}"


class FilterSettings(models.Model):
    """Persistent settings of a filter list."""

    ping_type = ArrayField(
        models.CharField(max_length=20),
        validators=(validate_ping_field,),
        help_text="Who to ping when this filter triggers."
    )
    filter_dm = models.BooleanField(help_text="Whether DMs should be filtered.")
    dm_ping_type = ArrayField(
        models.CharField(max_length=20),
        validators=(validate_ping_field,),
        help_text="Who to ping when this filter triggers on a DM."
    )
    delete_messages = models.BooleanField(
        help_text="Whether this filter should delete messages triggering it."
    )
    bypass_roles = ArrayField(
        models.BigIntegerField(),
        help_text="Roles and users who can bypass this filter."
    )
    enabled = models.BooleanField(
        help_text="Whether this filter is currently enabled."
    )
    default_action = models.ForeignKey(
        "FilterAction",
        models.CASCADE,
        help_text="What action to perform on the triggering user."
    )
    default_range = models.ForeignKey(
        "ChannelRange",
        models.CASCADE,
        help_text="The channels and categories in which this filter applies."
    )


class FilterAction(models.Model):
    """The action to take when a filter is triggered."""

    user_dm = models.CharField(
        max_length=1000,
        null=True,
        help_text="The DM to send to a user triggering this filter."
    )
    infraction_type = models.CharField(
        choices=InfractionType.choices,
        max_length=4,
        null=True,
        help_text="The infraction to apply to this user."
    )
    infraction_reason = models.CharField(
        max_length=1000,
        help_text="The reason to give for the infraction."
    )
    infraction_duration = models.DurationField(
        null=True,
        help_text="The duration of the infraction. Null if permanent."
    )


class ChannelRange(models.Model):
    """
    Where a filter should apply.

    The resolution is done in the following order:
    - disallowed channels
    - disallowed categories
    - allowed categories
    - allowed channels
    - default
    """

    disallowed_channels = ArrayField(models.IntegerField())
    disallowed_categories = ArrayField(models.IntegerField())
    allowed_channels = ArrayField(models.IntegerField())
    allowed_categories = ArrayField(models.IntegerField())
    default = models.BooleanField()


class Filter(models.Model):
    """One specific trigger of a list."""

    content = models.CharField(max_length=100, help_text="The definition of this filter.")
    description = models.CharField(max_length=200, help_text="Why this filter has been added.")
    additional_field = models.BooleanField(null=True, help_text="Implementation specific field.")
    override = models.ForeignKey(
        "FilterOverride",
        models.SET_NULL,
        null=True,
        help_text="Override the default settings."
    )

    def __str__(self) -> str:
        return f"Filter {self.content!r}"


class FilterOverride(models.Model):
    """
    Setting overrides of a specific filter.

    Any non-null value will override the default ones.
    """

    ping_type = ArrayField(
        models.CharField(max_length=20),
        validators=(validate_ping_field,), null=True
    )
    filter_dm = models.BooleanField(null=True)
    dm_ping_type = ArrayField(
        models.CharField(max_length=20),
        validators=(validate_ping_field,),
        null=True
    )
    delete_messages = models.BooleanField(null=True)
    bypass_roles = ArrayField(models.IntegerField(), null=True)
    enabled = models.BooleanField(null=True)
    filter_action = models.ForeignKey("FilterAction", models.CASCADE, null=True)
    filter_range = models.ForeignKey("ChannelRange", models.CASCADE, null=True)
