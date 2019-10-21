from django.test import TestCase
from django_hosts.resolvers import reverse


class TestIndexReturns200(TestCase):
    def test_index_returns_200(self):
        """Check that the index page returns a HTTP 200 response."""
        url = reverse('home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


class TestLoginCancelledReturns302(TestCase):
    def test_login_cancelled_returns_302(self):
        """Check that the login cancelled redirect returns a HTTP 302 response."""
        url = reverse('socialaccount_login_cancelled')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)


class TestLoginErrorReturns302(TestCase):
    def test_login_error_returns_302(self):
        """Check that the login error redirect returns a HTTP 302 response."""
        url = reverse('socialaccount_login_error')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
