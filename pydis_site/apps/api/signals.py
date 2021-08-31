from django.db.models.signals import pre_delete
from django.dispatch import receiver

from pydis_site.apps.api.models.bot import Role, User


@receiver(signal=pre_delete, sender=Role)
def delete_role_from_user(sender: Role, instance: Role, **kwargs) -> None:
    """Unassigns the Role (instance) that is being deleted from every user that has it."""
    for user in User.objects.filter(roles__contains=[instance.id]):
        del user.roles[user.roles.index(instance.id)]
        user.save()
