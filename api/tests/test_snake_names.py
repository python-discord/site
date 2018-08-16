from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import SnakeName



class StatusTests(APISubdomainTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_cannot_read_snake_name_list(self):
        url = reverse('bot:snakename-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_cannot_read_snake_names_with_get_all_param(self):
        url = reverse('bot:snakename-list', host='api')
        response = self.client.get(f'{url}?get_all=True')

        self.assertEqual(response.status_code, 401)


class EmptyDatabaseSnakeNameTests(APISubdomainTestCase):
    def test_endpoint_returns_empty_object(self):
        url = reverse('bot:snakename-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})

    def test_endpoint_returns_empty_list_with_get_all_param(self):
        url = reverse('bot:snakename-list', host='api')
        response = self.client.get(f'{url}?get_all=True')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


class SnakeNameListTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.snake_python = SnakeName.objects.create(name='Python', scientific='Totally.')

    def test_endpoint_returns_all_snakes_with_get_all_param(self):
        url = reverse('bot:snakename-list', host='api')
        response = self.client.get(f'{url}?get_all=True')

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
