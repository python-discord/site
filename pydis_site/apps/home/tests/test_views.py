from django.test import TestCase
from django.urls import reverse


class TestIndexReturns200(TestCase):
    def test_index_returns_200(self):
        """Check that the index page returns a HTTP 200 response."""
        url = reverse('home:home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
