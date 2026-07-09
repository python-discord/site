from datetime import UTC, datetime

from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from .base import AuthenticatedAPITestCase
from pydis_site.apps.api.models import MessageDeletionContext, User


class DeletedMessagesWithoutActorTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            id=55,
            name='Robbie Rotten',
            discriminator=55,
        )

        cls.data = {
            'actor': None,
            'creation': datetime.now(tz=UTC).isoformat(),
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
        url = reverse('api:bot:messagedeletioncontext-list')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 201)
        [context] = MessageDeletionContext.objects.all()
        self.assertIsNone(context.actor)


class DeletedMessagesQueryCountTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            id=77,
            name='Sportacus',
            discriminator=77,
        )

    def _build_data(self, message_count: int) -> dict:
        return {
            'actor': None,
            'creation': datetime.now(tz=UTC).isoformat(),
            'deletedmessage_set': [
                {
                    'author': self.author.id,
                    'id': 1000 + index,
                    'channel_id': 5555,
                    'content': f"Message {index}",
                    'embeds': [],
                    'attachments': []
                }
                for index in range(message_count)
            ]
        }

    def test_query_count_is_independent_of_message_count(self):
        """The number of queries must not grow with the size of the deletedmessage_set."""
        url = reverse('api:bot:messagedeletioncontext-list')

        with CaptureQueriesContext(connection) as few_ctx:
            response = self.client.post(url, data=self._build_data(2))
        self.assertEqual(response.status_code, 201)

        MessageDeletionContext.objects.all().delete()

        with CaptureQueriesContext(connection) as many_ctx:
            response = self.client.post(url, data=self._build_data(20))
        self.assertEqual(response.status_code, 201)

        self.assertEqual(len(few_ctx.captured_queries), len(many_ctx.captured_queries))



class DeletedMessagesWithActorTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = cls.actor = User.objects.create(
            id=12904,
            name='Joe Armstrong',
            discriminator=1245,
        )

        cls.data = {
            'actor': cls.actor.id,
            'creation': datetime.now(tz=UTC).isoformat(),
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
        url = reverse('api:bot:messagedeletioncontext-list')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 201)
        [context] = MessageDeletionContext.objects.all()
        self.assertEqual(context.actor.id, self.actor.id)


class DeletedMessagesLogURLTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = cls.actor = User.objects.create(
            id=324888,
            name='Black Knight',
            discriminator=1975,
        )

        cls.deletion_context = MessageDeletionContext.objects.create(
            actor=cls.actor,
            creation=datetime.now(tz=UTC),
        )

    def test_valid_log_url(self):
        [context] = MessageDeletionContext.objects.all()
        expected_url = reverse('staff:logs', args=(context.id,))
        self.assertEqual(context.log_url, expected_url)
