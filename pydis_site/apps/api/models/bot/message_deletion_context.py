from django.db import models

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.models.utils import ModelReprMixin


class MessageDeletionContext(ModelReprMixin, models.Model):
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
