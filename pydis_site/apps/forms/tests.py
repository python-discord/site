import secrets
import unittest.mock
from typing import Iterable

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from . import authentication
from . import models


def fake_user() -> models.DiscordUser:
    return models.DiscordUser(
        id=1234,
        username="Joe 'CIA' Banks",
        discriminator=1234,
        avatar=None,
        bot=True,
        system=True,
        locale="tr",
        verified=False,
        email="shredder@jeremiahboby.me",
        flags=0,
    )


def fake_member(user: models.DiscordUser, role_ids: tuple[int, ...]) -> models.DiscordMember:
    return models.DiscordMember(
        user=user,
        roles=role_ids,
        joined_at=timezone.now(),
        deaf=True,
        mute=False,
    )


class AuthenticatedTestCase(TestCase):
    """Allows testing the forms API as an authenticated user."""

    authenticate_as_admin = False
    """Whether to authenticate the test member as an administrator."""

    roles: tuple[str, ...] = ()
    """Which Discord role names to return for the given user."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = fake_user()
        cls.user.save()
        cls.addClassCleanup(cls.user.delete)

        roles_with_ids = tuple(models.DiscordRole(id=idx, name=name) for idx, name in enumerate(cls.roles))
        role_ids = tuple(role.id for role in roles_with_ids)
        cls.member = fake_member(cls.user, role_ids)
        cls.member.save()
        cls.addClassCleanup(cls.member.delete)

        get_roles_patcher = unittest.mock.patch("pydis_site.apps.forms.discord.get_roles")
        cls.patched_get_roles = get_roles_patcher.start()
        cls.patched_get_roles.return_value = roles_with_ids
        cls.addClassCleanup(get_roles_patcher.stop)

        if cls.authenticate_as_admin:
            admin = models.Admin(id=cls.member.id)
            admin.save()
            cls.addClassCleanup(admin.delete)

        cls.jwt_cookie = cls.create_jwt_cookie(cls.member)
        super().setUpClass()

    def setUp(self) -> None:
        self.jwt_login(self.member)
        super().setUp()

    @staticmethod
    def create_jwt_cookie(member: models.DiscordMember) -> str:
        data = {
            "token": secrets.token_urlsafe(6),
            "refresh": secrets.token_urlsafe(6),
            "user_details": {
                "id": member.id,
                "name": member.user.username,
            },
        }
        return "JWT " + authentication.encode_jwt(data)

    def jwt_login(self, member: models.DiscordMember) -> None:
        self.client.cookies["token"] = self.jwt_cookie


class TestIndex(TestCase):
    def test_index_returns_200(self) -> None:
        """The index page should return a HTTP 200 response."""

        url = reverse("forms:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


class TestAuthentication(TestCase):
    def tearDown(self) -> None:
        # Removes all cookies from the test client.
        self.client.logout()

    def run_test_with_cookie(self, cookie: str, error: str) -> None:
        url = reverse("forms:index")
        self.client.cookies["token"] = cookie
        resp = self.client.get(url)
        content = resp.json()
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(content, {"detail": error})

    def test_authentication_invalid_cookie_format(self) -> None:
        self.run_test_with_cookie(
            cookie="invalid prefix and token format",
            error="Unable to split prefix and token from authorization cookie.",
        )

    def test_authentication_invalid_cookie_prefix(self) -> None:
        self.run_test_with_cookie(cookie="mnesia: token", error="Invalid authorization cookie prefix 'mnesia:'.")

    @override_settings(SECRET_KEY="some-garbage", FORMS_SECRET_KEY="forms-key")
    def test_authentication_via_forms_secret_key(self) -> None:
        cookie = "JWT " + authentication.encode_jwt({}, signing_secret_key=settings.FORMS_SECRET_KEY)
        self.run_test_with_cookie(cookie=cookie, error="Token is missing from JWT.")

    @override_settings(SECRET_KEY="some-garbage", FORMS_SECRET_KEY="forms-key")
    def test_authentication_via_secret_key(self) -> None:
        cookie = "JWT " + authentication.encode_jwt({}, signing_secret_key=settings.SECRET_KEY)
        self.run_test_with_cookie(cookie=cookie, error="Token is missing from JWT.")

    def test_authentication_via_unknown_key(self) -> None:
        cookie = "JWT " + authentication.encode_jwt({}, signing_secret_key="JOEBANKS")
        self.run_test_with_cookie(cookie=cookie, error="Signature verification failed")

    def test_missing_refresh_token(self) -> None:
        content = {"token": "token"}
        cookie = "JWT " + authentication.encode_jwt(content, signing_secret_key=settings.SECRET_KEY)
        self.run_test_with_cookie(cookie=cookie, error="Refresh token is missing from JWT.")

    def test_missing_user_details(self) -> None:
        content = {"token": "token", "refresh": "refresh", "user_details": {"id": False}}
        cookie = "JWT " + authentication.encode_jwt(content, signing_secret_key=settings.SECRET_KEY)
        self.run_test_with_cookie(cookie=cookie, error="Could not parse user details.")

    def test_bad_user_details(self) -> None:
        content = {"token": "token", "refresh": "refresh", "user_details": ["erlang", "otp"]}
        cookie = "JWT " + authentication.encode_jwt(content, signing_secret_key=settings.SECRET_KEY)
        self.run_test_with_cookie(cookie=cookie, error="Could not parse user details.")


class NonAdminAuthenticationTest(AuthenticatedTestCase):
    def test_non_admin_user(self) -> None:
        url = reverse("forms:index")

        resp = self.client.get(url)
        content = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            content["user"],
            {
                "authenticated": True,
                "user": {"id": self.member.id, "name": self.member.user.username},
                "scopes": ["authenticated"],
            },
        )


class AdminAuthenticationTest(AuthenticatedTestCase):
    authenticate_as_admin = True

    def test_admin_user(self) -> None:
        url = reverse("forms:index")

        resp = self.client.get(url)
        content = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            content["user"],
            {
                "authenticated": True,
                "user": {"id": self.member.id, "name": self.member.user.username},
                "scopes": ["authenticated", "admin"],
            },
        )


class DiscordRolesTest(AuthenticatedTestCase):
    authenticate_as_admin = False
    roles = ("admin", "High Sharder")

    def test_admin_user(self) -> None:
        url = reverse("forms:index")

        resp = self.client.get(url)
        content = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            content["user"],
            {
                "authenticated": True,
                "user": {"id": self.member.id, "name": self.member.user.username},
                "scopes": ["authenticated", "High Sharder", "discord admin"],
            },
        )


# the ultimate power trip...
class DiscordAdminAndFormsAdminTest(AuthenticatedTestCase):
    authenticate_as_admin = True
    roles = ("admin",)

    def test_admin_user(self) -> None:
        url = reverse("forms:index")

        resp = self.client.get(url)
        content = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            content["user"],
            {
                "authenticated": True,
                "user": {"id": self.member.id, "name": self.member.user.username},
                "scopes": ["authenticated", "admin", "discord admin"],
            },
        )
