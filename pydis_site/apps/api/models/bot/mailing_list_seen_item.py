from django.db import models

from pydis_site.apps.api.models.mixins import ModelReprMixin
from .mailing_list import MailingList


class MailingListSeenItem(ModelReprMixin, models.Model):
    """An item in a mailing list that the bot has consumed and mirrored elsewhere."""

    list = models.ForeignKey(
        MailingList,
        on_delete=models.CASCADE,
        related_name='seen_items',
        help_text="The mailing list from which this seen item originates."
    )
    hash = models.CharField(
        max_length=100,
        help_text="A hash, or similar identifier, of the content that was seen."
    )

    class Meta:
        """Prevent adding the same hash to the same list multiple times."""

        constraints = (
            models.UniqueConstraint(
                fields=('list', 'hash'),
                name='unique_list_and_hash',
            ),
        )
