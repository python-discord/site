from django.db import models

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.models.mixins import ModelReprMixin


class Nomination(ModelReprMixin, models.Model):
    """A general helper nomination information created by staff."""

    active = models.BooleanField(
        default=True,
        help_text="Whether this nomination is still relevant."
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The nominated user.",
        related_name='nomination'
    )
    inserted_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The creation date of this nomination."
    )
    end_reason = models.TextField(
        help_text="Why the nomination was ended.",
        default="",
        blank=True
    )
    ended_at = models.DateTimeField(
        auto_now_add=False,
        help_text="When the nomination was ended.",
        null=True
    )
    reviewed = models.BooleanField(
        default=False,
        help_text="Whether voting message have been made."
    )

    def __str__(self):
        """Representation that makes the target and state of the nomination immediately evident."""
        status = "active" if self.active else "ended"
        return f"Nomination of {self.user} ({status})"

    class Meta:
        """Set the ordering of nominations to most recent first."""

        ordering = ("-inserted_at",)


class NominationEntry(ModelReprMixin, models.Model):
    """A nomination entry created by single staff."""

    nomination = models.ForeignKey(
        Nomination,
        on_delete=models.CASCADE,
        help_text="Nomination to what this entry belongs."
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The staff member that nominated this user.",
        related_name='nomination_set'
    )
    reason = models.TextField(
        help_text="Why the actor nominated this user.",
        null=True,
        blank=True
    )
    inserted_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The creation date of this nomination entry."
    )

    class Meta:
        """Meta options for NominationEntry model."""

        verbose_name_plural = "nomination entries"
