from datetime import datetime

from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import MessageDeletionContext, User


class DeletedMessagesWithoutActorTests(APISubdomainTestCase):
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
                    'embeds': [],
                    'attachments': []
                },
                {
                    'author': cls.author.id,
                    'id': 56,
                    'channel_id': 5555,
                    'content': "If you purge this, you're evil",
                    'embeds': [],
                    'attachments': []
                }
            ]
        }

    def test_accepts_valid_data(self):
        url = reverse('bot:messagedeletioncontext-list', host='api')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 201)
        [context] = MessageDeletionContext.objects.all()
        self.assertIsNone(context.actor)


class DeletedMessagesWithActorTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):  # noqa
        cls.author = cls.actor = User.objects.create(
            id=12904,
            name='Joe Armstrong',
            discriminator=1245,
            avatar_hash=None
        )

        cls.data = {
            'actor': cls.actor.id,
            'creation': datetime.utcnow().isoformat(),
            'deletedmessage_set': [
                {
                    'author': cls.author.id,
                    'id': 12903,
                    'channel_id': 1824,
                    'content': "I hate trailing commas",
                    'embeds': [],
                    'attachments': []
                },
            ]
        }

    def test_accepts_valid_data_and_sets_actor(self):
        url = reverse('bot:messagedeletioncontext-list', host='api')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 201)
        [context] = MessageDeletionContext.objects.all()
        self.assertEqual(context.actor.id, self.actor.id)
