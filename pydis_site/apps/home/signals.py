from contextlib import suppress
from typing import List, Optional, Type

from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount, SocialLogin
from allauth.socialaccount.providers.base import Provider
from allauth.socialaccount.providers.discord.provider import DiscordProvider
from allauth.socialaccount.signals import (
    pre_social_login, social_account_added, social_account_removed,
    social_account_updated)
from django.contrib.auth.models import Group, User as DjangoUser
from django.db.models.signals import post_delete, post_save, pre_save

from pydis_site.apps.api.models import User as DiscordUser
from pydis_site.apps.staff.models import RoleMapping


class AllauthSignalListener:
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
        post_save.connect(self.user_model_updated, sender=DiscordUser)

        post_delete.connect(self.mapping_model_deleted, sender=RoleMapping)
        pre_save.connect(self.mapping_model_updated, sender=RoleMapping)

        pre_social_login.connect(self.social_account_updated)
        social_account_added.connect(self.social_account_updated)
        social_account_updated.connect(self.social_account_updated)
        social_account_removed.connect(self.social_account_removed)

        user_logged_in.connect(self.user_logged_in)

    def user_logged_in(self, sender: Type[DjangoUser], **kwargs) -> None:
        """
        Processes Allauth login signals to ensure a user has the correct perms.

        This method tries to find a Discord SocialAccount for a user - this should always
        be the case, but the admin user likely won't have one, so we do check for it.

        After that, we try to find the user's stored Discord account details, provided by the
        bot on the server. Finally, we pass the relevant information over to the
        `_apply_groups()` method for final processing.
        """
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
        """
        Processes Allauth social account update signals to ensure a user has the correct perms.

        In this case, a SocialLogin is provided that we can check against. We check that this
        is a Discord login in order to ensure that future OAuth logins using other providers
        don't break things.

        Like most of the other methods that handle signals, this method defers to the
        `_apply_groups()` method for final processing.
        """
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
        """
        Processes Allauth social account reomval signals to ensure a user has the correct perms.

        In this case, a SocialAccount is provided that we can check against. If this is a
        Discord OAuth being removed from the account, we want to ensure that the user loses
        their permissions groups as well.

        While this isn't a realistic scenario to reach in our current setup, I've provided it
        for the sake of covering any edge cases and ensuring that SocialAccounts can be removed
        from Django users in the future if required.

        Like most of the other methods that handle signals, this method defers to the
        `_apply_groups()` method for final processing.
        """
        account: SocialAccount = kwargs["socialaccount"]
        provider: Provider = account.get_provider()

        if not isinstance(provider, DiscordProvider):
            return

        try:
            user: DiscordUser = DiscordUser.objects.get(id=int(account.uid))
        except DiscordUser.DoesNotExist:
            return

        self._apply_groups(user, account, deletion=True)

    def mapping_model_deleted(self, sender: Type[RoleMapping], **kwargs) -> None:
        """
        Processes deletion signals from the RoleMapping model, removing perms from users.

        We need to do this to ensure that users aren't left with permissions groups that
        they shouldn't have assigned to them when a RoleMapping is deleted from the database,
        and to remove their staff status if they should no longer have it.
        """
        instance: RoleMapping = kwargs["instance"]

        for user in instance.group.user_set.all():
            # Firstly, remove their related user group
            user.groups.remove(instance.group)

            with suppress(SocialAccount.DoesNotExist, DiscordUser.DoesNotExist):
                # If we get either exception, then the user could not have been assigned staff
                # with our system in the first place.

                social_account = SocialAccount.objects.get(user=user, provider=DiscordProvider.id)
                discord_user = DiscordUser.objects.get(id=int(social_account.uid))

                mappings = RoleMapping.objects.filter(role__id__in=discord_user.roles).all()
                is_staff = any(m.is_staff for m in mappings)

                if user.is_staff != is_staff:
                    user.is_staff = is_staff
                    user.save(update_fields=("is_staff", ))

    def mapping_model_updated(self, sender: Type[RoleMapping], **kwargs) -> None:
        """
        Processes update signals from the RoleMapping model.

        This method is in charge of figuring out what changed when a RoleMapping is updated
        (via the Django admin or otherwise). It operates based on what was changed, and can
        handle changes to both the role and permissions group assigned to it.
        """
        instance: RoleMapping = kwargs["instance"]
        raw: bool = kwargs["raw"]

        if raw:
            # Fixtures are being loaded, so don't touch anything
            return

        old_instance: Optional[RoleMapping] = None

        if instance.id is not None:
            # We don't try to catch DoesNotExist here because we can't test for it,
            # it should never happen (unless we have a bad DB failure) but I'm still
            # kind of antsy about not having the extra security here.

            old_instance = RoleMapping.objects.get(id=instance.id)

        if old_instance:
            self.mapping_model_deleted(RoleMapping, instance=old_instance)

        accounts = SocialAccount.objects.filter(
            uid__in=(u.id for u in DiscordUser.objects.filter(roles__contains=[instance.role.id]))
        )

        for account in accounts:
            account.user.groups.add(instance.group)

            if instance.is_staff and not account.user.is_staff:
                account.user.is_staff = instance.is_staff
                account.user.save(update_fields=("is_staff", ))
            else:
                discord_user = DiscordUser.objects.get(id=int(account.uid))

                mappings = RoleMapping.objects.filter(
                    role__id__in=discord_user.roles
                ).exclude(id=instance.id).all()
                is_staff = any(m.is_staff for m in mappings)

                if account.user.is_staff != is_staff:
                    account.user.is_staff = is_staff
                    account.user.save(update_fields=("is_staff",))

    def user_model_updated(self, sender: Type[DiscordUser], **kwargs) -> None:
        """
        Processes update signals from the Discord User model, assigning perms as required.

        When a user's roles are changed on the Discord server, this method will ensure that
        the user has only the permissions groups that they should have based on the RoleMappings
        that have been set up in the Django admin.

        Like some of the other signal handlers, this method ensures that a SocialAccount exists
        for this Discord User, and defers to `_apply_groups()` to do the heavy lifting of
        ensuring the permissions groups are correct.
        """
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
        """
        Ensures that the correct permissions are set for a Django user based on the RoleMappings.

        This (private) method is designed to check a Discord User against a given SocialAccount,
        and makes sure that the Django user associated with the SocialAccount has the correct
        permissions groups.

        While it would be possible to get the Discord User object with just the SocialAccount
        object, the current approach results in less queries.

        The `deletion` parameter is used to signify that the user's SocialAccount is about
        to be removed, and so we should always remove all of their permissions groups. The
        same thing will happen if the user is no longer actually on the Discord server, as
        leaving the server does not currently remove their SocialAccount from the database.
        """
        mappings = RoleMapping.objects.all()

        try:
            current_groups: List[Group] = list(account.user.groups.all())
        except SocialAccount.user.RelatedObjectDoesNotExist:
            return  # There's no user account yet, this will be handled by another receiver

        # Ensure that the username on this account is correct
        new_username = f"{user.name}#{user.discriminator}"

        if account.user.username != new_username:
            account.user.username = new_username
            account.user.first_name = new_username

        if not user.in_guild:
            deletion = True

        if deletion:
            # They've unlinked Discord or left the server, so we have to remove their groups
            # and their staff status

            if current_groups:
                # They do have groups, so let's remove them
                account.user.groups.remove(
                    *(mapping.group for mapping in mappings)
                )

            if account.user.is_staff:
                # They're marked as a staff user and they shouldn't be, so let's fix that
                account.user.is_staff = False
        else:
            new_groups = []
            is_staff = False

            for role in user.roles:
                try:
                    mapping = mappings.get(role__id=role)
                except RoleMapping.DoesNotExist:
                    continue  # No mapping exists

                new_groups.append(mapping.group)

                if mapping.is_staff:
                    is_staff = True

            account.user.groups.add(
                *[group for group in new_groups if group not in current_groups]
            )

            account.user.groups.remove(
                *[mapping.group for mapping in mappings if mapping.group not in new_groups]
            )

            if account.user.is_staff != is_staff:
                account.user.is_staff = is_staff

        account.user.save()
