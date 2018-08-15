from django_hosts.resolvers import reverse
from rest_framework.test import APITestCase, force_authenticate


class EmptyDatabaseSnakeNameTests(APITestCase):
    def test_endpoint_returns_empty_list(self):
        import pdb; pdb.set_trace()
        url = reverse('snake-names-list', host='api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
