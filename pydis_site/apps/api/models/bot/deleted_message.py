from django.db import models

from pydis_site.apps.api.models.bot.message import Message
from pydis_site.apps.api.models.bot.message_deletion_context import MessageDeletionContext


class DeletedMessage(Message):
    """A deleted message, previously sent somewhere on the Discord server."""

    deletion_context = models.ForeignKey(
        MessageDeletionContext,
        help_text="The deletion context this message is part of.",
        on_delete=models.CASCADE
    )

    class Meta:
        """Sets the default ordering for list views to newest first."""

        ordering = ("-id",)
