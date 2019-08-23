from datetime import datetime as dt, timezone

from django.test import SimpleTestCase

from ..models import (
    DeletedMessage, DocumentationLink,
    Infraction, Message,
    MessageDeletionContext, ModelReprMixin,
    OffTopicChannelName, Reminder,
    Role, Tag, User
)


class SimpleClass(ModelReprMixin):
    def __init__(self, is_what):
        self.the_cake = is_what


class ReprMixinTests(SimpleTestCase):
    def setUp(self):
        self.klass = SimpleClass('is a lie')

    def test_shows_attributes(self):
        expected = "<SimpleClass(the_cake='is a lie')>"
        self.assertEqual(repr(self.klass), expected)


class StringDunderMethodTests(SimpleTestCase):
    def setUp(self):
        self.objects = (
            DeletedMessage(
                id=45,
                author=User(
                    id=444, name='bill',
                    discriminator=5, avatar_hash=None
                ),
                channel_id=666,
                content="wooey",
                deletion_context=MessageDeletionContext(
                    actor=User(
                        id=5555, name='shawn',
                        discriminator=555, avatar_hash=None
                    ),
                    creation=dt.utcnow()
                ),
                embeds=[]
            ),
            DocumentationLink(
                'test', 'http://example.com', 'http://example.com'
            ),
            OffTopicChannelName(name='bob-the-builders-playground'),
            Role(
                id=5, name='test role',
                colour=0x5, permissions=0,
                position=10,
            ),
            Message(
                id=45,
                author=User(
                    id=444, name='bill',
                    discriminator=5, avatar_hash=None
                ),
                channel_id=666,
                content="wooey",
                embeds=[]
            ),
            MessageDeletionContext(
                actor=User(
                    id=5555, name='shawn',
                    discriminator=555, avatar_hash=None
                ),
                creation=dt.utcnow()
            ),
            Tag(
                title='bob',
                embed={'content': "the builder"}
            ),
            User(
                id=5, name='bob',
                discriminator=1, avatar_hash=None
            ),
            Infraction(
                user_id=5, actor_id=5,
                type='kick', reason='He terk my jerb!'
            ),
            Infraction(
                user_id=5, actor_id=5, hidden=True,
                type='kick', reason='He terk my jerb!',
                expires_at=dt(5018, 11, 20, 15, 52, tzinfo=timezone.utc)
            ),
            Reminder(
                author=User(
                    id=452, name='billy',
                    discriminator=5, avatar_hash=None
                ),
                channel_id=555,
                content="oh no",
                expiration=dt(5018, 11, 20, 15, 52, tzinfo=timezone.utc)
            )
        )

    def test_returns_string(self):
        for instance in self.objects:
            self.assertIsInstance(str(instance), str)
