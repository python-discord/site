from unittest.mock import patch

from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.models import SocialAccount, SocialLogin
from django.contrib.auth.models import User
from django.contrib.messages.storage.base import BaseStorage
from django.http import HttpRequest
from django.test import TestCase

from pydis_site.utils.account import AccountAdapter, SocialAccountAdapter


class AccountUtilsTests(TestCase):
    def setUp(self):
        self.django_user = User.objects.create(username="user")

        self.discord_account = SocialAccount.objects.create(
            user=self.django_user, provider="discord", uid=0
        )

        self.github_account = SocialAccount.objects.create(
            user=self.django_user, provider="github", uid=0
        )

    def test_account_adapter(self):
        """Test that our Allauth account adapter functions correctly."""
        adapter = AccountAdapter()

        self.assertFalse(adapter.is_open_for_signup(HttpRequest()))

    def test_social_account_adapter(self):
        """Test that our Allauth social account adapter functions correctly."""
        adapter = SocialAccountAdapter()

        discord_login = SocialLogin(account=self.discord_account)
        github_login = SocialLogin(account=self.github_account)

        messages_request = HttpRequest()
        messages_request._messages = BaseStorage(messages_request)

        with patch("pydis_site.utils.account.reverse") as mock_reverse:
            with patch("pydis_site.utils.account.redirect") as mock_redirect:
                with self.assertRaises(ImmediateHttpResponse):
                    adapter.is_open_for_signup(messages_request, github_login)

                self.assertEqual(len(messages_request._messages._queued_messages), 1)
                self.assertEqual(mock_redirect.call_count, 1)
            self.assertEqual(mock_reverse.call_count, 1)

        self.assertTrue(adapter.is_open_for_signup(HttpRequest(), discord_login))
