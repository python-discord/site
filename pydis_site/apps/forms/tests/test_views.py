from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .base import AuthenticatedTestCase
from pydis_site.apps.forms.models import Admin


class IndexTestCase(TestCase):
    def test_index_returns_200(self) -> None:
        """The index page should return a HTTP 200 response."""

        url = reverse("forms:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


class UnauthorizedAdminTestCase(TestCase):
    def test_create_admin_unauthorized(self) -> None:
        """The POST /admin URL should return an error without auth."""

        url = reverse("forms:admin")
        resp = self.client.post(url, {"hello": "world"})
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)


class ForbiddenAdminTestCase(AuthenticatedTestCase):
    def test_create_admin_forbidden(self) -> None:
        """The POST /admin URL should return an error without the required scopes."""

        url = reverse("forms:admin")
        resp = self.client.post(url, {"hello": "world"})
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)


class AdminTestCase(AuthenticatedTestCase):
    authenticate_as_admin = True

    def test_create_admin_fresh(self) -> None:
        """Creating an admin should work when an admin makes the request."""

        url = reverse("forms:admin")
        resp = self.client.post(url, {"id": 1234})
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        admin = Admin.objects.get(id=1234)
        self.assertIsNotNone(admin)
        resp = self.client.post(url, {"id": 1234})
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(resp.json()["error"], "already_exists")

    def test_create_admin_missing_field(self) -> None:
        """Creating an admin should require the `id` field to be sent."""

        url = reverse("forms:admin")
        resp = self.client.post(url, {"oranges and lemons": "say the bells of st clement's"})
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(resp.json()["error"], "which-id-please")
