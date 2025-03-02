from pathlib import Path

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

TESTING_RESOURCES_PATH = Path(
    settings.BASE_DIR, "pydis_site", "apps", "resources", "tests", "testing_resources"
)


class TestResourcesView(TestCase):
    def test_resources_index_200(self):
        """Check does index of resources app return 200 HTTP response."""
        url = reverse("resources:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_resources_with_valid_argument(self):
        """Check that you can resolve the resources when passing a valid argument."""
        url = reverse("resources:index", kwargs={"resource_type": "book"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_resources_with_invalid_argument(self):
        """Check that you can resolve the resources when passing an invalid argument."""
        url = reverse("resources:index", kwargs={"resource_type": "urinal-cake"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestResourceFilterView(TestCase):
    def test_resource_filter_response(self):
        """Check that the filter endpoint returns JSON-formatted filters."""
        url = reverse('resources:filters')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertIn('difficulty', content)
        self.assertIsInstance(content['difficulty'], list)
