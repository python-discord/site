from django_hosts.resolvers import reverse

from pydis_site.apps.api.models import FilterList
from pydis_site.apps.api.tests.base import APISubdomainTestCase

URL = reverse('bot:filterlist-list', host='api')
JPEG_ALLOWLIST = {
    "type": 'FILE_FORMAT',
    "allowed": True,
    "content": ".jpeg",
}
PNG_ALLOWLIST = {
    "type": 'FILE_FORMAT',
    "allowed": True,
    "content": ".png",
}


class UnauthenticatedTests(APISubdomainTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_cannot_read_allowedlist_list(self):
        response = self.client.get(URL)

        self.assertEqual(response.status_code, 401)


class EmptyDatabaseTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        FilterList.objects.all().delete()

    def test_returns_empty_object(self):
        response = self.client.get(URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


class FetchTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        FilterList.objects.all().delete()
        cls.jpeg_format = FilterList.objects.create(**JPEG_ALLOWLIST)
        cls.png_format = FilterList.objects.create(**PNG_ALLOWLIST)

    def test_returns_name_in_list(self):
        response = self.client.get(URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["content"], self.jpeg_format.content)
        self.assertEqual(response.json()[1]["content"], self.png_format.content)

    def test_returns_single_item_by_id(self):
        response = self.client.get(f'{URL}/{self.jpeg_format.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("content"), self.jpeg_format.content)

    def test_returns_filter_list_types(self):
        response = self.client.get(f'{URL}/get-types')

        self.assertEqual(response.status_code, 200)
        for api_type, model_type in zip(response.json(), FilterList.FilterListType.choices):
            self.assertEquals(api_type[0], model_type[0])
            self.assertEquals(api_type[1], model_type[1])


class CreationTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        FilterList.objects.all().delete()

    def test_returns_400_for_missing_params(self):
        no_type_json = {
            "allowed": True,
            "content": ".jpeg"
        }
        no_allowed_json = {
            "type": "FILE_FORMAT",
            "content": ".jpeg"
        }
        no_content_json = {
            "allowed": True,
            "type": "FILE_FORMAT"
        }
        cases = [{}, no_type_json, no_allowed_json, no_content_json]

        for case in cases:
            with self.subTest(case=case):
                response = self.client.post(URL, data=case)
                self.assertEqual(response.status_code, 400)

    def test_returns_201_for_successful_creation(self):
        response = self.client.post(URL, data=JPEG_ALLOWLIST)
        self.assertEqual(response.status_code, 201)

    def test_returns_400_for_duplicate_creation(self):
        self.client.post(URL, data=JPEG_ALLOWLIST)
        response = self.client.post(URL, data=JPEG_ALLOWLIST)
        self.assertEqual(response.status_code, 400)


class DeletionTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        FilterList.objects.all().delete()
        cls.jpeg_format = FilterList.objects.create(**JPEG_ALLOWLIST)
        cls.png_format = FilterList.objects.create(**PNG_ALLOWLIST)

    def test_deleting_unknown_id_returns_404(self):
        response = self.client.delete(f"{URL}/200")
        self.assertEqual(response.status_code, 404)

    def test_deleting_known_id_returns_204(self):
        response = self.client.delete(f"{URL}/{self.jpeg_format.id}")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"{URL}/{self.jpeg_format.id}")
        self.assertNotIn(self.png_format.content, response.json())
