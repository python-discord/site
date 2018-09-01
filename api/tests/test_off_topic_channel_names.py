from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import OffTopicChannelName


class UnauthenticatedTests(APISubdomainTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_cannot_read_off_topic_channel_name_list(self):
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_cannot_read_off_topic_channel_name_list_with_random_item_param(self):
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(f'{url}?random_items=no')

        self.assertEqual(response.status_code, 401)


class EmptyDatabaseTests(APISubdomainTestCase):
    def test_returns_empty_object(self):
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_returns_empty_list_with_get_all_param(self):
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(f'{url}?random_items=5')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_returns_400_for_bad_random_items_param(self):
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(f'{url}?random_items=totally-a-valid-integer')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'random_items': "Must be a valid integer."})


class ListRouteTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_name = OffTopicChannelName.objects.create(name='lemons-lemonade-stand')

    def test_returns_name_in_list(self):
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                self.test_name.name
            ]
        )

    def test_returns_name_in_list_with_random_items_param(self):
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(f'{url}?random_items=1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                self.test_name.name
            ]
        )
