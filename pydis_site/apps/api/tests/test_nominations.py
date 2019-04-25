from datetime import datetime as dt, timedelta, timezone

from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import Nomination, User


# class NominationTests(APISubdomainTestCase):
#     @classmethod
#     def setUpTestData(cls):  # noqa
#         cls.actor = User.objects.create(
#             id=5152,
#             name='Ro Bert',
#             discriminator=256,
#             avatar_hash=None
#         )
#         cls.user = cls.actor

#         cls.nomination = Nomination.objects.create(
#             actor=cls.actor,
#             reason="he's good",
#             user=cls.actor
#         )

#     def test_returns_400_on_attempt_to_update_frozen_field(self):
#         url = reverse('bot:nomination-detail', args=(self.user.id,), host='api')
#         response = self.client.put(
#             url,
#             data={'inserted_at': 'something bad'}
#         )
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json(), {
#             'inserted_at': ['This field cannot be updated.']
#         })

#     def test_returns_200_on_successful_update(self):
#         url = reverse('bot:nomination-detail', args=(self.user.id,), host='api')
#         response = self.client.patch(
#             url,
#             data={'reason': 'there are many like it, but this test is mine'}
#         )
#         self.assertEqual(response.status_code, 200)


class CreationTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):  # noqa
        cls.user = User.objects.create(
            id=1234,
            name='joe dart',
            discriminator=1111,
            avatar_hash=None
        )

    def test_accepts_valid_data(self):
        url = reverse('bot:nomination-list', host='api')
        data = {
            'actor': self.user.id,
            'reason': 'Joe Dart on Fender Bass',
            'user': self.user.id,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

        nomination = Nomination.objects.get(id=response.json()['id'])
        self.assertAlmostEqual(
            nomination.inserted_at,
            dt.now(timezone.utc),
            delta=timedelta(seconds=2)
        )
