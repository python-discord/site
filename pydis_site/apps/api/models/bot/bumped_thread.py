from django.core.validators import MinValueValidator
from django.db import models

from pydis_site.apps.api.models.mixins import ModelReprMixin


class BumpedThread(ModelReprMixin, models.Model):
    """A list of thread IDs to be bumped."""

    thread_id = models.BigIntegerField(
        primary_key=True,
        help_text=(
            "The thread ID that should be bumped."
        ),
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Thread IDs cannot be negative."
            ),
        ),
        verbose_name="Thread ID",
    )
