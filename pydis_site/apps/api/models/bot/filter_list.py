from django.db import models

from pydis_site.apps.api.models.mixins import ModelReprMixin, ModelTimestampMixin


class FilterList(ModelTimestampMixin, ModelReprMixin, models.Model):
    """An item that is either allowed or denied."""

    FilterListType = models.TextChoices(
        'FilterListType',
        'GUILD_INVITE '
        'FILE_FORMAT '
        'DOMAIN_NAME '
        'FILTER_TOKEN '
    )
    type = models.CharField(
        max_length=50,
        help_text="The type of allowlist this is on.",
        choices=FilterListType.choices,
    )
    allowed = models.BooleanField(
        help_text="Whether this item is on the allowlist or the denylist."
    )
    content = models.TextField(
        help_text="The data to add to the allow or denylist."
    )
    comment = models.TextField(
        help_text="Optional comment on this entry.",
        null=True
    )
