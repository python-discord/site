from typing import List, Type

from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount, SocialLogin
from allauth.socialaccount.providers.base import Provider
from allauth.socialaccount.providers.discord.provider import DiscordProvider
from allauth.socialaccount.signals import (
    pre_social_login, social_account_added, social_account_removed,
    social_account_updated)
from django.contrib.auth.models import Group, User as DjangoUser
from django.db.models.signals import post_save

from pydis_site.apps.api.models import User as DiscordUser
from pydis_site.apps.staff.models import RoleMapping


class SignalListener:
    """
    Listens to and processes events via the Django Signals system.

    Django Signals is basically an event dispatcher. It consists of Signals (which are the events)
    and Receivers, which listen for and handle those events. Signals are triggered by Senders,
    which are essentially just any class at all, and Receivers can filter the Signals they listen
    for by choosing a Sender, if required.

    Signals themselves define a set of arguments that they will provide to Receivers when the
    Signal is sent. They are always keyword arguments, and Django recommends that all Receiver
    functions accept them as `**kwargs` (and will supposedly error if you don't do this),
    supposedly because Signals can change in the future and your receivers should still work.

    Signals do provide a list of their arguments when they're initially constructed, but this
    is purely for documentation purposes only and Django does not enforce it.

    The Django Signals docs are here: https://docs.djangoproject.com/en/2.2/topics/signals/
    """

    def __init__(self):
        post_save.connect(self.model_updated, sender=DiscordUser)

        pre_social_login.connect(self.social_account_updated)
        social_account_added.connect(self.social_account_updated)
        social_account_updated.connect(self.social_account_updated)
        social_account_removed.connect(self.social_account_removed)

        user_logged_in.connect(self.user_login)

    def user_login(self, sender: Type[DjangoUser], **kwargs) -> None:
        """Handles signals relating to Allauth logins."""
        user: DjangoUser = kwargs["user"]

        try:
            account: SocialAccount = SocialAccount.objects.get(
                user=user, provider=DiscordProvider.id
            )
        except SocialAccount.DoesNotExist:
            return  # User's never linked a Discord account

        try:
            discord_user: DiscordUser = DiscordUser.objects.get(id=int(account.uid))
        except DiscordUser.DoesNotExist:
            return

        self._apply_groups(discord_user, account)

    def social_account_updated(self, sender: Type[SocialLogin], **kwargs) -> None:
        """Handle signals relating to new/existing social accounts."""
        social_login: SocialLogin = kwargs["sociallogin"]

        account: SocialAccount = social_login.account
        provider: Provider = account.get_provider()

        if not isinstance(provider, DiscordProvider):
            return

        try:
            user: DiscordUser = DiscordUser.objects.get(id=int(account.uid))
        except DiscordUser.DoesNotExist:
            return

        self._apply_groups(user, account)

    def social_account_removed(self, sender: Type[SocialLogin], **kwargs) -> None:
        """Handle signals relating to removal of social accounts."""
        account: SocialAccount = kwargs["socialaccount"]
        provider: Provider = account.get_provider()

        if not isinstance(provider, DiscordProvider):
            return

        try:
            user: DiscordUser = DiscordUser.objects.get(id=int(account.uid))
        except DiscordUser.DoesNotExist:
            return

        self._apply_groups(user, account, True)

    def model_updated(self, sender: Type[DiscordUser], **kwargs) -> None:
        """Handle signals related to the updating of Discord User model entries."""
        instance: DiscordUser = kwargs["instance"]
        raw: bool = kwargs["raw"]

        # `update_fields` could be used for checking changes, but it's None here due to how the
        # model is saved without using that argument - so we can't use it.

        if raw:
            # Fixtures are being loaded, so don't touch anything
            return

        try:
            account: SocialAccount = SocialAccount.objects.get(
                uid=str(instance.id), provider=DiscordProvider.id
            )
        except SocialAccount.DoesNotExist:
            return  # User has never logged in with Discord on the site

        self._apply_groups(instance, account)

    def _apply_groups(
            self, user: DiscordUser, account: SocialAccount, deletion: bool = False
    ) -> None:
        mappings = RoleMapping.objects.all()

        try:
            current_groups: List[Group] = list(account.user.groups.all())
        except SocialAccount.user.RelatedObjectDoesNotExist:
            return  # There's no user account yet, this will be handled by another receiver

        if not user.in_guild:
            deletion = True

        if deletion:
            # They've unlinked Discord or left the server, so we have to remove their groups

            if not current_groups:
                return  # They have no groups anyway, no point in processing

            account.user.groups.remove(
                *(mapping.group for mapping in mappings)
            )
        else:
            new_groups = []

            for role in user.roles.all():
                try:
                    new_groups.append(mappings.get(role=role).group)
                except RoleMapping.DoesNotExist:
                    continue  # No mapping exists

            remove_groups = [
                mapping.group for mapping in mappings if mapping.group not in new_groups
            ]

            add_groups = [group for group in new_groups if group not in current_groups]

            if remove_groups:
                account.user.groups.remove(*remove_groups)

            if add_groups:
                account.user.groups.add(*add_groups)
