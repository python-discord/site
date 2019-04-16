from django.test import TestCase
from django_hosts.resolvers import reverse

from pydis_site.apps.home.templatetags import extra_filters


class TestIndexReturns200(TestCase):
    def test_index_returns_200(self):
        url = reverse('home.index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


class TestExtraFilterTemplateTags(TestCase):
    def test_starts_with(self):
        self.assertTrue(extra_filters.starts_with('foo', 'f'))
