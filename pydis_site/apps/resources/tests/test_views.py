from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django_hosts import reverse

TESTING_RESOURCES_PATH = Path(
    settings.BASE_DIR, "pydis_site", "apps", "resources", "tests", "testing_resources"
)


class TestResourcesView(TestCase):
    def test_resources_index_200(self):
        """Check does index of resources app return 200 HTTP response."""
        url = reverse("resources:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestResourcesListView(TestCase):
    def test_valid_resource_list_200(self):
        """Check does site return code 200 when visiting valid resource list."""
        url = reverse("resources:resources")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @patch("pydis_site.apps.resources.resource_search.RESOURCES_PATH", TESTING_RESOURCES_PATH)
    def test_filter_resource_list(self):
        """TODO: Check that we can correctly filter resources with GET parameters."""
        pass
