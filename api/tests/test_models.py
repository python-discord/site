from datetime import datetime as dt, timezone

from django.test import SimpleTestCase

from ..models import (
    DocumentationLink, Infraction,
    ModelReprMixin, OffTopicChannelName,
    Role, SnakeFact, SnakeIdiom,
    SnakeName, SpecialSnake,
    Tag, User
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
            DocumentationLink(
                'test', 'http://example.com', 'http://example.com'
            ),
            OffTopicChannelName(name='bob-the-builders-playground'),
            SnakeFact(fact='snakes are cute'),
            SnakeIdiom(idiom='snake snacks'),
            SnakeName(name='python', scientific='3'),
            SpecialSnake(
                name='Pythagoras Pythonista',
                info='The only python snake that is born a triangle'
            ),
            Role(
                id=5, name='test role',
                colour=0x5, permissions=0
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
                user_id=5, actor_id=5, hidden=True,
                type='kick', reason='He terk my jerb!',
                expires_at=dt(5018, 11, 20, 15, 52, tzinfo=timezone.utc)
            )
        )

    def test_returns_string(self):
        for instance in self.objects:
            self.assertIsInstance(str(instance), str)
