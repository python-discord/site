from django.db import models

from pydis_site.apps.api.models import ModelReprMixin, ModelTimestampMixin


class AllowList(ModelTimestampMixin, ModelReprMixin, models.Model):
    """An item that is either allowed or denied."""

    AllowListType = models.TextChoices(
        'guild_invite_id',
        'file_format',
        'domain_name',
        'word_watchlist',
    )
    type = models.CharField(
        max_length=50,
        help_text=(
            "The type of allowlist this is on. The value must be one of the following: "
            f"{','.join(AllowListType.choices)}."
        ),
        choices=AllowListType.choices,
    )
    allowed = models.BooleanField(
        help_text="Whether this item is on the allowlist or the denylist."
    )
    content = models.TextField(
        help_text="The data to add to the allowlist."
    )
