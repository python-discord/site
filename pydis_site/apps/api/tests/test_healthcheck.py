from django.urls import reverse

from .base import AuthenticatedAPITestCase


class UnauthedHealthcheckAPITests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_can_access_healthcheck_view(self):
        url = reverse('api:healthcheck')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})
