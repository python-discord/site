from django.test import TestCase
from django_hosts.resolvers import reverse


class TestIndexReturns200(TestCase):
    def test_index_returns_200(self):
        url = reverse('home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


class TestLoginCancelledReturns302(TestCase):
    def test_login_cancelled_returns_302(self):
        url = reverse('socialaccount_login_cancelled')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)


class TestLoginErrorReturns302(TestCase):
    def test_login_error_returns_302(self):
        url = reverse('socialaccount_login_error')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
