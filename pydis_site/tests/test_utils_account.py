from unittest.mock import patch

from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.models import SocialAccount, SocialLogin
from django.contrib.auth.models import User
from django.contrib.messages.storage.base import BaseStorage
from django.http import HttpRequest
from django.test import RequestFactory, TestCase

from pydis_site.apps.api.models import Role, User as DiscordUser
from pydis_site.utils.account import AccountAdapter, SocialAccountAdapter


class AccountUtilsTests(TestCase):
    def setUp(self):
        # Create the user
        self.django_user = User.objects.create(username="user")

        # Create the roles
        developers_role = Role.objects.create(
            id=1,
            name="Developers",
            colour=0,
            permissions=0,
            position=1
        )
        everyone_role = Role.objects.create(
            id=0,
            name="@everyone",
            colour=0,
            permissions=0,
            position=0
        )

        # Create the social accounts
        self.discord_account = SocialAccount.objects.create(
            user=self.django_user, provider="discord", uid=0
        )
        self.discord_account_one_role = SocialAccount.objects.create(
            user=self.django_user, provider="discord", uid=1
        )
        self.discord_account_two_roles = SocialAccount.objects.create(
            user=self.django_user, provider="discord", uid=2
        )
        self.discord_account_not_present = SocialAccount.objects.create(
            user=self.django_user, provider="discord", uid=3
        )
        self.github_account = SocialAccount.objects.create(
            user=self.django_user, provider="github", uid=0
        )

        # Create DiscordUsers
        self.discord_user = DiscordUser.objects.create(
            id=0,
            name="user",
            discriminator=0
        )

        self.discord_user_role = DiscordUser.objects.create(
            id=1,
            name="user present",
            discriminator=0,
            roles=[everyone_role.id]
        )

        self.discord_user_two_roles = DiscordUser.objects.create(
            id=2,
            name="user with both roles",
            discriminator=0,
            roles=[everyone_role.id, developers_role.id]
        )

        self.request_factory = RequestFactory()

    def test_account_adapter(self):
        """Test that our Allauth account adapter functions correctly."""
        adapter = AccountAdapter()

        self.assertFalse(adapter.is_open_for_signup(HttpRequest()))

    def test_social_account_adapter_signup(self):
        """Test that our Allauth social account adapter correctly handles signups."""
        adapter = SocialAccountAdapter()

        discord_login = SocialLogin(account=self.discord_account)
        discord_login_role = SocialLogin(account=self.discord_account_one_role)
        discord_login_not_present = SocialLogin(account=self.discord_account_not_present)
        discord_login_two_roles = SocialLogin(account=self.discord_account_two_roles)

        github_login = SocialLogin(account=self.github_account)

        messages_request = self.request_factory.get("/")
        messages_request._messages = BaseStorage(messages_request)

        with patch("pydis_site.utils.account.reverse") as mock_reverse:
            with patch("pydis_site.utils.account.redirect") as mock_redirect:
                with self.assertRaises(ImmediateHttpResponse):
                    adapter.is_open_for_signup(messages_request, github_login)

                with self.assertRaises(ImmediateHttpResponse):
                    adapter.is_open_for_signup(messages_request, discord_login)

                with self.assertRaises(ImmediateHttpResponse):
                    adapter.is_open_for_signup(messages_request, discord_login_role)

                with self.assertRaises(ImmediateHttpResponse):
                    adapter.is_open_for_signup(messages_request, discord_login_not_present)

                self.assertTrue(
                    adapter.is_open_for_signup(messages_request, discord_login_two_roles)
                )

                self.assertEqual(len(messages_request._messages._queued_messages), 4)
                self.assertEqual(mock_redirect.call_count, 4)
            self.assertEqual(mock_reverse.call_count, 4)

    def test_social_account_adapter_populate(self):
        """Test that our Allauth social account adapter correctly handles data population."""
        adapter = SocialAccountAdapter()

        discord_login = SocialLogin(
            account=self.discord_account,
            user=self.django_user
        )
        discord_login.account.extra_data["discriminator"] = "0000"

        discord_user = adapter.populate_user(
            self.request_factory.get("/"), discord_login,
            {"username": "user"}
        )
        self.assertEqual(discord_user.username, "user#0000")
        self.assertEqual(discord_user.first_name, "user#0000")

        discord_login.account.provider = "not_discord"
        not_discord_user = adapter.populate_user(
            self.request_factory.get("/"), discord_login,
            {"username": "user"}
        )
        self.assertEqual(not_discord_user.username, "user")
