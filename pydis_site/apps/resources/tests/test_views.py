from django.test import TestCase
from django_hosts import reverse


class TestResourcesView(TestCase):
    def test_resources_index_200(self):
        """Check does index of resources app return 200 HTTP response."""
        url = reverse("resources:resources")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
