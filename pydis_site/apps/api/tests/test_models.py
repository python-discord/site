from datetime import UTC, datetime as dt

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase

from pydis_site.apps.api.models import (
    DeletedMessage,
    DocumentationLink,
    Filter,
    FilterList,
    Infraction,
    MessageDeletionContext,
    Nomination,
    NominationEntry,
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


class NitroMessageLengthTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=50, name='bill', discriminator=5)
        self.context = MessageDeletionContext.objects.create(
            id=50,
            actor=self.user,
            creation=dt.now(UTC)
        )

    def test_create(self):
        message = DeletedMessage(
            id=46,
            author=self.user,
            channel_id=666,
            content="w"*4000,
            deletion_context=self.context,
            embeds=[]
        )

        try:
            message.clean_fields()
        except Exception as e:  # pragma: no cover
            self.fail(f"Creation of message of length 3950 failed with: {e}")

    def test_create_failure(self):
        message = DeletedMessage(
            id=47,
            author=self.user,
            channel_id=666,
            content="w"*4001,
            deletion_context=self.context,
            embeds=[]
        )

        self.assertRaisesRegex(ValidationError, "content':", message.clean_fields)


class StringDunderMethodTests(SimpleTestCase):
    def setUp(self):
        self.nomination = Nomination(
            id=123,
            user=User(
                id=9876,
                name="Hemlock's Cat",
                discriminator=7777,
            ),
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
                    creation=dt.now(UTC)
                ),
                embeds=[]
            ),
            DocumentationLink(
                'test', 'http://example.com', 'http://example.com'
            ),
            FilterList(
                name="forbidden_duckies",
                list_type=0,
            ),
            Filter(
                content="ducky_nsfw",
                description="This ducky is totally inappropriate!",
                additional_settings=None,
            ),
            OffensiveMessage(
                id=602951077675139072,
                channel_id=291284109232308226,
                delete_date=dt(3000, 1, 1, tzinfo=UTC)
            ),
            OffTopicChannelName(name='bob-the-builders-playground'),
            Role(
                id=5, name='test role',
                colour=0x5, permissions=0,
                position=10,
            ),
            MessageDeletionContext(
                actor=User(
                    id=5555,
                    name='shawn',
                    discriminator=555,
                ),
                creation=dt.now(tz=UTC)
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
                expires_at=dt(5018, 11, 20, 15, 52, tzinfo=UTC)
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
                expiration=dt(5018, 11, 20, 15, 52, tzinfo=UTC)
            ),
            NominationEntry(
                nomination_id=self.nomination.id,
                actor=User(
                    id=9876,
                    name='Mr. Hemlock',
                    discriminator=6666,
                ),
                reason="He purrrrs like the best!",
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


class UserTests(SimpleTestCase):
    def test_str_without_discriminator(self) -> None:
        user = User(name="lemonfannumber1")
        self.assertEqual(str(user), "lemonfannumber1")
