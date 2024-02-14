from django.db import models

from pydis_site.apps.api.models.mixins import ModelReprMixin


class MailingList(ModelReprMixin, models.Model):
    """A mailing list that the bot is following."""

    name = models.CharField(
        max_length=50,
        help_text="A short identifier for the mailing list.",
        unique=True
    )
