from django.db import models
from django_hosts.resolvers import reverse

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.models.mixins import ModelReprMixin


class MessageDeletionContext(ModelReprMixin, models.Model):
    """
    Represents the context for a deleted message.

    The context includes its creation date, as well as the actor associated with the deletion.
    This helps to keep track of message deletions on the server.
    """

    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=(
            "The original actor causing this deletion. Could be the author "
            "of a manual clean command invocation, the bot when executing "
            "automatic actions, or nothing to indicate that the bulk "
            "deletion was not issued by us."
        ),
        null=True
    )
    creation = models.DateTimeField(
        # Consider whether we want to add a validator here that ensures
        # the deletion context does not take place in the future.
        help_text="When this deletion took place."
    )

    @property
    def log_url(self) -> str:
        """Create the url for the deleted message logs."""
        return reverse('logs', host="staff", args=(self.id,))

    class Meta:
        """Set the ordering for list views to newest first."""

        ordering = ("-creation",)
