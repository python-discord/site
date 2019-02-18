from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import Nomination, User


class NominationTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):  # noqa
        cls.author = User.objects.create(
            id=5152,
            name='Ro Bert',
            discriminator=256,
            avatar_hash=None
        )
        cls.user = cls.author

        cls.nomination = Nomination.objects.create(
            author=cls.author,
            reason="he's good",
            user=cls.author
        )

    def test_returns_400_on_attempt_to_update_frozen_field(self):
        url = reverse('bot:nomination-detail', args=(self.user.id,), host='api')
        response = self.client.put(
            url,
            data={'inserted_at': 'something bad'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'inserted_at': ['This field cannot be updated.']
        })

    def test_returns_200_on_successful_update(self):
        url = reverse('bot:nomination-detail', args=(self.user.id,), host='api')
        response = self.client.patch(
            url,
            data={'reason': 'there are many like it, but this test is mine'}
        )
        self.assertEqual(response.status_code, 200)
