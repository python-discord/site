from datetime import datetime

from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import User


class DeletedMessagesTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):  # noqa
        cls.author = User.objects.create(
            id=55,
            name='Robbie Rotten',
            discriminator=55,
            avatar_hash=None
        )

        cls.data = {
            'actor': None,
            'creation': datetime.utcnow().isoformat(),
            'deletedmessage_set': [
                {
                    'author': cls.author.id,
                    'id': 55,
                    'channel_id': 5555,
                    'content': "Terror Billy is a meanie",
                    'embeds': []
                },
                {
                    'author': cls.author.id,
                    'id': 56,
                    'channel_id': 5555,
                    'content': "If you purge this, you're evil",
                    'embeds': []
                }
            ]
        }

    def test_accepts_valid_data(self):
        url = reverse('bot:messagedeletioncontext-list', host='api')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 201)
