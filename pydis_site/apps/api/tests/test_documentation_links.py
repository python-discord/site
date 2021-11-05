from django.urls import reverse

from .base import AuthenticatedAPITestCase
from ..models import DocumentationLink


class UnauthedDocumentationLinkAPITests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_detail_lookup_returns_401(self):
        url = reverse('api:bot:documentationlink-detail', args=('whatever',))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_list_returns_401(self):
        url = reverse('api:bot:documentationlink-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_create_returns_401(self):
        url = reverse('api:bot:documentationlink-list')
        response = self.client.post(url, data={'hi': 'there'})

        self.assertEqual(response.status_code, 401)

    def test_delete_returns_401(self):
        url = reverse('api:bot:documentationlink-detail', args=('whatever',))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 401)


class EmptyDatabaseDocumentationLinkAPITests(AuthenticatedAPITestCase):
    def test_detail_lookup_returns_404(self):
        url = reverse('api:bot:documentationlink-detail', args=('whatever',))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_list_all_returns_empty_list(self):
        url = reverse('api:bot:documentationlink-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_delete_returns_404(self):
        url = reverse('api:bot:documentationlink-detail', args=('whatever',))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)


class DetailLookupDocumentationLinkAPITests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.doc_link = DocumentationLink.objects.create(
            package='testpackage',
            base_url='https://example.com/',
            inventory_url='https://example.com'
        )

        cls.doc_json = {
            'package': cls.doc_link.package,
            'base_url': cls.doc_link.base_url,
            'inventory_url': cls.doc_link.inventory_url
        }

    def test_detail_lookup_unknown_package_returns_404(self):
        url = reverse('api:bot:documentationlink-detail', args=('whatever',))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_detail_lookup_created_package_returns_package(self):
        url = reverse('api:bot:documentationlink-detail', args=(self.doc_link.package,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.doc_json)

    def test_list_all_packages_shows_created_package(self):
        url = reverse('api:bot:documentationlink-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.doc_json])

    def test_create_invalid_body_returns_400(self):
        url = reverse('api:bot:documentationlink-list')
        response = self.client.post(url, data={'i': 'am', 'totally': 'valid'})

        self.assertEqual(response.status_code, 400)

    def test_create_invalid_url_returns_400(self):
        body = {
            'package': 'example',
            'base_url': 'https://example.com',
            'inventory_url': 'totally an url'
        }

        url = reverse('api:bot:documentationlink-list')
        response = self.client.post(url, data=body)

        self.assertEqual(response.status_code, 400)

    def test_create_invalid_package_name_returns_400(self):
        test_cases = ("InvalidPackage", "invalid package", "i\u0150valid")
        for case in test_cases:
            with self.subTest(package_name=case):
                body = self.doc_json.copy()
                body['package'] = case
                url = reverse('api:bot:documentationlink-list')
                response = self.client.post(url, data=body)

                self.assertEqual(response.status_code, 400)


class DocumentationLinkCreationTests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()

        self.body = {
            'package': 'example',
            'base_url': 'https://example.com/',
            'inventory_url': 'https://docs.example.com'
        }

        url = reverse('api:bot:documentationlink-list')
        response = self.client.post(url, data=self.body)

        self.assertEqual(response.status_code, 201)

    def test_package_in_full_list(self):
        url = reverse('api:bot:documentationlink-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.body])

    def test_detail_lookup_works_with_package(self):
        url = reverse('api:bot:documentationlink-detail', args=(self.body['package'],))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.body)


class DocumentationLinkDeletionTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.doc_link = DocumentationLink.objects.create(
            package='example',
            base_url='https://example.com',
            inventory_url='https://docs.example.com'
        )

    def test_unknown_package_returns_404(self):
        url = reverse('api:bot:documentationlink-detail', args=('whatever',))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

    def test_delete_known_package_returns_204(self):
        url = reverse('api:bot:documentationlink-detail', args=(self.doc_link.package,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
