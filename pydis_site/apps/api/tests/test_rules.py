import itertools
import re
from pathlib import Path

from django.urls import reverse

from .base import AuthenticatedAPITestCase
from pydis_site.apps.api.views import RulesView


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


class RuleCorrectnessTests(AuthenticatedAPITestCase):
    """Verifies that the rules from the API and by the static rules in the content app match."""

    @classmethod
    def setUpTestData(cls):
        cls.markdown_rule_re = re.compile(r'^> \d+\. (.*)$')

    def test_rules_in_markdown_file_roughly_equal_api_rules(self) -> None:
        url = reverse('api:rules')
        api_response = self.client.get(url + '?link_format=md')
        api_rules = tuple(rule for (rule, _tags) in api_response.json())

        markdown_rules_path = (
            Path(__file__).parent.parent.parent / 'content' / 'resources' / 'rules.md'
        )

        markdown_rules = []
        for line in markdown_rules_path.read_text().splitlines():
            matches = self.markdown_rule_re.match(line)
            if matches is not None:
                markdown_rules.append(matches.group(1))

        zipper = itertools.zip_longest(api_rules, markdown_rules)
        for idx, (api_rule, markdown_rule) in enumerate(zipper):
            with self.subTest(f"Rule {idx}"):
                self.assertIsNotNone(
                    markdown_rule, f"The API has more rules than {markdown_rules_path}"
                )
                self.assertIsNotNone(
                    api_rule, f"{markdown_rules_path} has more rules than the API endpoint"
                )
                self.assertEqual(markdown_rule, api_rule)
