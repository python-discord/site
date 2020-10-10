from django.db import models
from django.utils import timezone

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.models.mixins import ModelReprMixin


class Infraction(ModelReprMixin, models.Model):
    """An infraction for a Discord user."""

    TYPE_CHOICES = (
        ("note", "Note"),
        ("warning", "Warning"),
        ("watch", "Watch"),
        ("mute", "Mute"),
        ("kick", "Kick"),
        ("ban", "Ban"),
        ("superstar", "Superstar"),
        ("voice_ban", "Voice Ban"),
    )
    inserted_at = models.DateTimeField(
        default=timezone.now,
        help_text="The date and time of the creation of this infraction."
    )
    expires_at = models.DateTimeField(
        null=True,
        help_text=(
            "The date and time of the expiration of this infraction. "
            "Null if the infraction is permanent or it can't expire."
        )
    )
    active = models.BooleanField(
        help_text="Whether the infraction is still active."
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='infractions_received',
        help_text="The user to which the infraction was applied."
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='infractions_given',
        help_text="The user which applied the infraction."
    )
    type = models.CharField(
        max_length=9,
        choices=TYPE_CHOICES,
        help_text="The type of the infraction."
    )
    reason = models.TextField(
        null=True,
        help_text="The reason for the infraction."
    )
    hidden = models.BooleanField(
        default=False,
        help_text="Whether the infraction is a shadow infraction."
    )

    def __str__(self):
        """Returns some info on the current infraction, for display purposes."""
        s = f"#{self.id}: {self.type} on {self.user_id}"
        if self.expires_at:
            s += f" until {self.expires_at}"
        if self.hidden:
            s += " (hidden)"
        return s

    class Meta:
        """Defines the meta options for the infraction model."""

        ordering = ['-inserted_at']
        constraints = (
            models.UniqueConstraint(
                fields=["user", "type"],
                condition=models.Q(active=True),
                name="unique_active_infraction_per_type_per_user"
            ),
        )
