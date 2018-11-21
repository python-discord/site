from datetime import datetime as dt, timedelta, timezone
from urllib.parse import quote

from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import Infraction, User


class InfractionTests(APISubdomainTestCase):
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
            hidden=True,
            expires_at=dt(5018, 11, 20, 15, 52, tzinfo=timezone.utc)
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

    def test_partial_update(self):
        url = reverse('bot:infraction-detail', args=(self.ban_hidden.id,), host='api')
        data = {
            'expires_at': '4143-02-15T21:04:31+00:00',
            'active': False,
            'reason': 'durka derr',
            'id': 12,
            'inserted_at': '4143-02-15T21:04:31+00:00',
            'user': 6,
            'actor': 6,
            'type': 'kick',
            'hidden': False
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
        infraction = Infraction.objects.get(id=self.ban_hidden.id)

        # Updates for these fields were accepted.
        self.assertEqual(infraction.expires_at.isoformat(), data['expires_at'])
        self.assertEqual(infraction.active, data['active'])
        self.assertEqual(infraction.reason, data['reason'])

        # Updates for these fields were ignored.
        self.assertEqual(infraction.id, self.ban_hidden.id)
        self.assertEqual(infraction.inserted_at, self.ban_hidden.inserted_at)
        self.assertEqual(infraction.user.id, self.ban_hidden.user.id)
        self.assertEqual(infraction.actor.id, self.ban_hidden.actor.id)
        self.assertEqual(infraction.type, self.ban_hidden.type)
        self.assertEqual(infraction.hidden, self.ban_hidden.hidden)


class CreationTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):  # noqa
        cls.user = User.objects.create(
            id=5,
            name='james',
            discriminator=1,
            avatar_hash=None
        )

    def test_accepts_valid_data(self):
        url = reverse('bot:infraction-list', host='api')
        data = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'ban',
            'reason': 'He terk my jerb!',
            'hidden': True,
            'expires_at': '5018-11-20T15:52:00+00:00'
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

        infraction = Infraction.objects.get(id=1)
        self.assertAlmostEqual(
            infraction.inserted_at,
            dt.now(timezone.utc),
            delta=timedelta(seconds=2)
        )
        self.assertEqual(infraction.expires_at.isoformat(), data['expires_at'])
        self.assertEqual(infraction.user.id, data['user'])
        self.assertEqual(infraction.actor.id, data['actor'])
        self.assertEqual(infraction.type, data['type'])
        self.assertEqual(infraction.reason, data['reason'])
        self.assertEqual(infraction.hidden, data['hidden'])
        self.assertEqual(infraction.active, True)

    def test_returns_400_for_missing_user(self):
        url = reverse('bot:infraction-list', host='api')
        data = {
            'actor': self.user.id,
            'type': 'kick'
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'user': ['This field is required.']
        })

    def test_returns_400_for_bad_user(self):
        url = reverse('bot:infraction-list', host='api')
        data = {
            'user': 1337,
            'actor': self.user.id,
            'type': 'kick'
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'user': ['Invalid pk "1337" - object does not exist.']
        })

    def test_returns_400_for_bad_type(self):
        url = reverse('bot:infraction-list', host='api')
        data = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'hug'
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'type': ['"hug" is not a valid choice.']
        })

    def test_returns_400_for_bad_timestamp(self):
        url = reverse('bot:infraction-list', host='api')
        data = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'ban',
            'expires_at': '20/11/5018 15:52:00'
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'expires_at': [
                'Datetime has wrong format. Use one of these formats instead: '
                'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'
            ]
        })
