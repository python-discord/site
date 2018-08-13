from django.shortcuts import reverse
from django.test import TestCase


class TestIndexReturns200(TestCase):
    def test_index_returns_200(self):
        url = reverse('home:index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
