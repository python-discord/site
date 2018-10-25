from django.test import SimpleTestCase

from ..models import (
    DocumentationLink, Member, ModelReprMixin,
    OffTopicChannelName, Role,
    SnakeFact, SnakeIdiom,
    SnakeName, SpecialSnake,
    Tag
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
            SpecialSnake(name='Pythagoras Pythonista',
                         info='The only python snake that is born a triangle'),
            Role(
                id=5, name='test role',
                colour=0x5, permissions=0
            ),
            Member(
                id=5, name='bob',
                discriminator=1, avatar_hash=None
            ),
            Tag(
                title='bob',
                embed={'content': "the builder"}
            )
        )

    def test_returns_string(self):
        for instance in self.objects:
            self.assertIsInstance(str(instance), str)
