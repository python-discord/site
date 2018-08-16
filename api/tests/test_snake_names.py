from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import SnakeName



class StatusTests(APISubdomainTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_cannot_read_snake_names(self):
        url = reverse('snakename-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)


class EmptyDatabaseSnakeNameTests(APISubdomainTestCase):
    def test_endpoint_unauthed_returns_empty_list(self):
        url = reverse('snakename-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


class SnakeNameListTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.snake_python = SnakeName.objects.create(name='Python', scientific='Totally.')

    def test_endpoint_returns_all_snakes(self):
        url = reverse('snakename-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'name': 'Python',
                    'scientific': 'Totally.'
                }
            ]
        )
