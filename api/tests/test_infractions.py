from urllib.parse import quote

from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import Infraction, User


class ListTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):  # noqa
        cls.user = User.objects.create(
            id=5,
            name='james',
            discriminator=1,
            avatar_hash=None
        )
        cls.ban_hidden = Infraction.objects.create(
            user_id=cls.user.id,
            actor_id=cls.user.id,
            type='ban',
            reason='He terk my jerb!',
            hidden=True
        )
        cls.ban_inactive = Infraction.objects.create(
            user_id=cls.user.id,
            actor_id=cls.user.id,
            type='ban',
            reason='James is an ass, and we won\'t be working with him again.',
            active=False
        )

    def test_list_all(self):
        url = reverse('bot:infraction-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        infractions = response.json()

        self.assertEqual(len(infractions), 2)
        self.assertEqual(infractions[0]['id'], self.ban_hidden.id)
        self.assertEqual(infractions[1]['id'], self.ban_inactive.id)

    def test_filter_search(self):
        url = reverse('bot:infraction-list', host='api')
        pattern = quote(r'^James(\s\w+){3},')
        response = self.client.get(f'{url}?search={pattern}')

        self.assertEqual(response.status_code, 200)
        infractions = response.json()

        self.assertEqual(len(infractions), 1)
        self.assertEqual(infractions[0]['id'], self.ban_inactive.id)

    def test_filter_field(self):
        url = reverse('bot:infraction-list', host='api')
        response = self.client.get(f'{url}?type=ban&hidden=true')

        self.assertEqual(response.status_code, 200)
        infractions = response.json()

        self.assertEqual(len(infractions), 1)
        self.assertEqual(infractions[0]['id'], self.ban_hidden.id)

    def test_returns_empty_for_no_match(self):
        url = reverse('bot:infraction-list', host='api')
        response = self.client.get(f'{url}?type=ban&search=poop')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_retrieve_single_from_id(self):
        url = reverse('bot:infraction-detail', args=(self.ban_inactive.id,), host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.ban_inactive.id)
