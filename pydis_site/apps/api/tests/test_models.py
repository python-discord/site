from datetime import datetime as dt

from django.test import SimpleTestCase
from django.utils import timezone

from pydis_site.apps.api.models import (
    DeletedMessage,
    DocumentationLink,
    Infraction,
    Message,
    MessageDeletionContext,
    Nomination,
    OffTopicChannelName,
    OffensiveMessage,
    Reminder,
    Role,
    User
)
from pydis_site.apps.api.models.mixins import ModelReprMixin


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
        self.nomination = Nomination(
            id=123,
            actor=User(
                id=9876,
                name='Mr. Hemlock',
                discriminator=6666,
            ),
            user=User(
                id=9876,
                name="Hemlock's Cat",
                discriminator=7777,
            ),
            reason="He purrrrs like the best!",
        )

        self.objects = (
            DeletedMessage(
                id=45,
                author=User(
                    id=444,
                    name='bill',
                    discriminator=5,
                ),
                channel_id=666,
                content="wooey",
                deletion_context=MessageDeletionContext(
                    actor=User(
                        id=5555,
                        name='shawn',
                        discriminator=555,
                    ),
                    creation=dt.utcnow()
                ),
                embeds=[]
            ),
            DocumentationLink(
                'test', 'http://example.com', 'http://example.com'
            ),
            OffensiveMessage(
                id=602951077675139072,
                channel_id=291284109232308226,
                delete_date=dt(3000, 1, 1)
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
                    id=444,
                    name='bill',
                    discriminator=5,
                ),
                channel_id=666,
                content="wooey",
                embeds=[]
            ),
            MessageDeletionContext(
                actor=User(
                    id=5555,
                    name='shawn',
                    discriminator=555,
                ),
                creation=dt.utcnow()
            ),
            User(
                id=5,
                name='bob',
                discriminator=1,
            ),
            Infraction(
                user_id=5,
                actor_id=5,
                type='kick',
                reason='He terk my jerb!'
            ),
            Infraction(
                user_id=5,
                actor_id=5,
                hidden=True,
                type='kick',
                reason='He terk my jerb!',
                expires_at=dt(5018, 11, 20, 15, 52, tzinfo=timezone.utc)
            ),
            Reminder(
                author=User(
                    id=452,
                    name='billy',
                    discriminator=5,
                ),
                channel_id=555,
                jump_url=(
                    'https://discordapp.com/channels/'
                    '267624335836053506/291284109232308226/463087129459949587'
                ),
                content="oh no",
                expiration=dt(5018, 11, 20, 15, 52, tzinfo=timezone.utc)
            )
        )

    def test_returns_string(self):
        for instance in self.objects:
            self.assertIsInstance(str(instance), str)

    def test_nomination_str_representation(self):
        self.assertEqual(
            "Nomination of Hemlock's Cat#7777 (active)",
            str(self.nomination)
        )
