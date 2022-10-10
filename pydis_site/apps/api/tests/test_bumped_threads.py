from django.urls import reverse

from .base import AuthenticatedAPITestCase
from ..models import BumpedThread


class UnauthedBumpedThreadAPITests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_detail_lookup_returns_401(self):
        url = reverse('api:bot:bumpedthread-detail', args=(1,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_list_returns_401(self):
        url = reverse('api:bot:bumpedthread-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_create_returns_401(self):
        url = reverse('api:bot:bumpedthread-list')
        response = self.client.post(url, {"thread_id": 3})

        self.assertEqual(response.status_code, 401)

    def test_delete_returns_401(self):
        url = reverse('api:bot:bumpedthread-detail', args=(1,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 401)


class BumpedThreadAPITests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.thread1 = BumpedThread.objects.create(
            thread_id=1234,
        )

    def test_returns_bumped_threads_as_flat_list(self):
        url = reverse('api:bot:bumpedthread-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [1234])

    def test_returns_204_for_existing_data(self):
        url = reverse('api:bot:bumpedthread-detail', args=(1234,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")

    def test_returns_404_for_non_existing_data(self):
        url = reverse('api:bot:bumpedthread-detail', args=(42,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Not found."})
