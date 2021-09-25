from abc import abstractmethod
from typing import List

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

from pydis_site.apps.api.models.mixins import AbstractModelMeta


class FilterListType(models.IntegerChoices):
    """Choice between allow or deny for a list type."""

    ALLOW = 1
    DENY = 0


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


class FilterSettingsMixin(models.Model, metaclass=AbstractModelMeta):
    """Mixin for settings of a filter list."""

    @staticmethod
    @abstractmethod
    def allow_null() -> bool:
        """Abstract property for allowing null values."""

    ping_type = ArrayField(
        models.CharField(max_length=20),
        validators=(validate_ping_field,),
        help_text="Who to ping when this filter triggers.",
        null=allow_null.__func__()
    )
    filter_dm = models.BooleanField(help_text="Whether DMs should be filtered.", null=True)
    dm_ping_type = ArrayField(
        models.CharField(max_length=20),
        validators=(validate_ping_field,),
        help_text="Who to ping when this filter triggers on a DM.",
        null=allow_null.__func__()
    )
    delete_messages = models.BooleanField(
        help_text="Whether this filter should delete messages triggering it.",
        null=allow_null.__func__()
    )
    bypass_roles = ArrayField(
        models.BigIntegerField(),
        help_text="Roles and users who can bypass this filter.",
        null=allow_null.__func__()
    )
    enabled = models.BooleanField(
        help_text="Whether this filter is currently enabled.",
        null=allow_null.__func__()
    )
    dm_content = models.CharField(
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

    # Where a filter should apply.
    #
    # The resolution is done in the following order:
    #   - disallowed channels
    #   - disallowed categories
    #   - allowed categories
    #   - allowed channels
    disallowed_channels = ArrayField(models.IntegerField())
    disallowed_categories = ArrayField(models.IntegerField())
    allowed_channels = ArrayField(models.IntegerField())
    allowed_categories = ArrayField(models.IntegerField())

    class Meta:
        """Metaclass for settings mixin."""

        abstract = True


class FilterList(FilterSettingsMixin):
    """Represent a list in its allow or deny form."""

    name = models.CharField(max_length=50, help_text="The unique name of this list.")
    list_type = models.IntegerField(
        choices=FilterListType.choices,
        help_text="Whether this list is an allowlist or denylist"
    )

    @staticmethod
    def allow_null() -> bool:
        """Do not allow null values for default settings."""
        return False

    class Meta:
        """Constrain name and list_type unique."""

        constraints = (
            UniqueConstraint(fields=("name", "list_type"), name="unique_name_type"),
        )

    def __str__(self) -> str:
        return f"Filter {FilterListType(self.list_type).label}list {self.name!r}"


class Filter(FilterSettingsMixin):
    """One specific trigger of a list."""

    content = models.CharField(max_length=100, help_text="The definition of this filter.")
    description = models.CharField(max_length=200, help_text="Why this filter has been added.")
    additional_field = models.BooleanField(null=True, help_text="Implementation specific field.")
    filter_list = models.ForeignKey(
        FilterList, models.CASCADE, related_name="filters",
        help_text="The filter list containing this filter."
    )

    def __str__(self) -> str:
        return f"Filter {self.content!r}"

    @staticmethod
    def allow_null() -> bool:
        """Allow null values for overrides."""
        return True
