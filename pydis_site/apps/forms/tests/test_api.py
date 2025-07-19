
from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

from pydis_site.apps.forms import authentication
from pydis_site.apps.forms.tests.base import AuthenticatedTestCase


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
