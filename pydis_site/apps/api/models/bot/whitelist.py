from django.db import models

from pydis_site.apps.api.models.utils import ModelReprMixin


class Whitelist(ModelReprMixin, models.Model):
    """Whitelisted item for a type."""

    INVITE = "invite"
    EXTENSION = "extension"
    CHANNEL = "channel"
    ROLE = "role"
    TYPE_CHOICES = (
        ("invite", "invite"),
        ("extension", "extension"),
        ("channel", "channel"),
        ("role", "role")
    )
    type = models.CharField(
        choices=TYPE_CHOICES,
        max_length=100,
        help_text=(
            "Type of the whitelisted item."
        ),
    )
    whitelisted_item = models.CharField(
        max_length=300,
        help_text=(
            "whitelisted item"
        )
    )

    def __str__(self):
        """Returns the whitelisted_item, for display purposes."""
        return self.whitelisted_item

    class Meta:
        """Defines the meta options for the Whitelist model."""

        unique_together = ("type", "whitelisted_item")
