from django.urls import reverse

from .base import AuthenticatedAPITestCase
from ..views import RulesView


class RuleAPITests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_can_access_rules_view(self):
        url = reverse('api:rules')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_link_format_query_param_produces_different_results(self):
        url = reverse('api:rules')
        markdown_links_response = self.client.get(url + '?link_format=md')
        html_links_response = self.client.get(url + '?link_format=html')
        self.assertNotEqual(
            markdown_links_response.json(),
            html_links_response.json()
        )

    def test_format_link_raises_value_error_for_invalid_target(self):
        with self.assertRaises(ValueError):
            RulesView._format_link("a", "b", "c")

    def test_get_returns_400_for_wrong_link_format(self):
        url = reverse('api:rules')
        response = self.client.get(url + '?link_format=unknown')
        self.assertEqual(response.status_code, 400)
