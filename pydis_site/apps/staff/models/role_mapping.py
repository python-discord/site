from django.contrib.auth.models import Group
from django.db import models

from pydis_site.apps.api.models import Role


class RoleMapping(models.Model):
    """A mapping between a Discord role and Django permissions group."""

    role = models.OneToOneField(
        Role,
        on_delete=models.CASCADE,
        help_text="The Discord role to use for this mapping.",
        unique=True,  # Unique in order to simplify group assignment logic
    )

    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        help_text="The Django permissions group to use for this mapping.",
        unique=True,  # Unique in order to simplify group assignment logic
    )

    is_staff = models.BooleanField(
        help_text="Whether this role mapping relates to a Django staff group",
        default=False
    )

    def __str__(self):
        """Returns the mapping, for display purposes."""
        return f"@{self.role.name} -> {self.group.name}"
