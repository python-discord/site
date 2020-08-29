from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import OffTopicChannelName


class UnauthenticatedTests(APISubdomainTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_cannot_read_off_topic_channel_name_list(self):
        """Return a 401 response when not authenticated."""
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_cannot_read_off_topic_channel_name_list_with_random_item_param(self):
        """Return a 401 response when `random_items` provided and not authenticated."""
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(f'{url}?random_items=no')

        self.assertEqual(response.status_code, 401)


class EmptyDatabaseTests(APISubdomainTestCase):
    def test_returns_empty_object(self):
        """Return empty list when no names in database."""
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_returns_empty_list_with_get_all_param(self):
        """Return empty list when no names and `random_items` param provided."""
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(f'{url}?random_items=5')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_returns_400_for_bad_random_items_param(self):
        """Return error message when passing not integer as `random_items`."""
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(f'{url}?random_items=totally-a-valid-integer')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'random_items': ["Must be a valid integer."]
        })

    def test_returns_400_for_negative_random_items_param(self):
        """Return error message when passing negative int as `random_items`."""
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(f'{url}?random_items=-5')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'random_items': ["Must be a positive integer."]
        })


class ListTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_name = OffTopicChannelName.objects.create(name='lemons-lemonade-stand', used=False)
        cls.test_name_2 = OffTopicChannelName.objects.create(name='bbq-with-bisk', used=True)

    def test_returns_name_in_list(self):
        """Return all off-topic channel names."""
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                self.test_name.name,
                self.test_name_2.name
            ]
        )

    def test_returns_single_item_with_random_items_param_set_to_1(self):
        """Return not-used name instead used."""
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(f'{url}?random_items=1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json(), [self.test_name.name])

    def test_running_out_of_names_with_random_parameter(self):
        """Reset names `used` parameter to `False` when running out of names."""
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(f'{url}?random_items=2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.test_name.name, self.test_name_2.name])


class CreationTests(APISubdomainTestCase):
    def setUp(self):
        super().setUp()

        url = reverse('bot:offtopicchannelname-list', host='api')
        self.name = "abcdefghijklmnopqrstuvwxyz-0123456789"
        response = self.client.post(f'{url}?name={self.name}')
        self.assertEqual(response.status_code, 201)

    def test_returns_201_for_unicode_chars(self):
        """Accept all valid characters."""
        url = reverse('bot:offtopicchannelname-list', host='api')
        names = (
            '𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹',
            'ǃ？’',
        )

        for name in names:
            response = self.client.post(f'{url}?name={name}')
            self.assertEqual(response.status_code, 201)

    def test_returns_400_for_missing_name_param(self):
        """Return error message when name not provided."""
        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'name': ["This query parameter is required."]
        })

    def test_returns_400_for_bad_name_param(self):
        """Return error message when invalid characters provided."""
        url = reverse('bot:offtopicchannelname-list', host='api')
        invalid_names = (
            'space between words',
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            '!?\'@#$%^&*()',
        )

        for name in invalid_names:
            response = self.client.post(f'{url}?name={name}')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {
                'name': ["Enter a valid value."]
            })


class DeletionTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_name = OffTopicChannelName.objects.create(name='lemons-lemonade-stand')
        cls.test_name_2 = OffTopicChannelName.objects.create(name='bbq-with-bisk')

    def test_deleting_unknown_name_returns_404(self):
        """Return 404 reponse when trying to delete unknown name."""
        url = reverse('bot:offtopicchannelname-detail', args=('unknown-name',), host='api')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

    def test_deleting_known_name_returns_204(self):
        """Return 204 response when deleting was successful."""
        url = reverse('bot:offtopicchannelname-detail', args=(self.test_name.name,), host='api')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

    def test_name_gets_deleted(self):
        """Name gets actually deleted."""
        url = reverse('bot:offtopicchannelname-detail', args=(self.test_name_2.name,), host='api')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

        url = reverse('bot:offtopicchannelname-list', host='api')
        response = self.client.get(url)
        self.assertNotIn(self.test_name_2.name, response.json())
