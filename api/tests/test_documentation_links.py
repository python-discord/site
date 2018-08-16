from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import DocumentationLink


class UnauthedDocumentationLinkAPITests(APISubdomainTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_detail_lookup_returns_401(self):
        url = reverse('bot:documentationlink-detail', args=('whatever',), host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_list_returns_401(self):
        url = reverse('bot:documentationlink-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

class EmptyDatabaseDocumentationLinkAPITests(APISubdomainTestCase):
    def test_detail_lookup_returns_404(self):
        url = reverse('bot:documentationlink-detail', args=('whatever',), host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_list_all_returns_empty_list(self):
        url = reverse('bot:documentationlink-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


class DetailLookupDocumentationLinkAPITests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.doc_link = DocumentationLink.objects.create(
            package='testpackage',
            base_url='https://example.com',
            inventory_url='https://example.com'
        )

        cls.doc_json = {
            'package': cls.doc_link.package,
            'base_url': cls.doc_link.base_url,
            'inventory_url': cls.doc_link.inventory_url
        }

    def test_detail_lookup_unknown_package_returns_404(self):
        url = reverse('bot:documentationlink-detail', args=('whatever',), host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_detail_lookup_created_package_returns_package(self):
        url = reverse('bot:documentationlink-detail', args=(self.doc_link.package,), host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.doc_json)

    def test_list_all_packages_shows_created_package(self):
        url = reverse('bot:documentationlink-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.doc_json])
