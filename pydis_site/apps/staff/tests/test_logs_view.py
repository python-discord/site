from django.test import Client, TestCase
from django.utils import timezone
from django_hosts.resolvers import reverse, reverse_host

from pydis_site.apps.api.models.bot import DeletedMessage, MessageDeletionContext, Role, User
from ..templatetags.deletedmessage_filters import hex_colour


class TestLogsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.developers_role = Role.objects.create(
            id=12345678,
            name="Developers",
            colour=16777215,
            permissions=104324673,
            position=1,
        )

        cls.author = cls.actor = User.objects.create(
            id=12345678901,
            name='Alan Turing',
            discriminator=1912,
            avatar_hash=None
        )

        cls.author.roles.add(cls.developers_role)

        cls.deletion_context = MessageDeletionContext.objects.create(
            actor=cls.actor,
            creation=timezone.now()
        )

        cls.deleted_message = DeletedMessage.objects.create(
            author=cls.author,
            id=614125807161573397,
            channel_id=1984,
            content='I think my tape has run out...',
            embeds=[],
            deletion_context=cls.deletion_context,
        )

    def setUp(self):
        """Sets up a test client that automatically sets the correct HOST header."""
        self.client = Client(HTTP_HOST=reverse_host(host="staff"))

    def test_logs_returns_200_for_existing_logs_pk(self):
        url = reverse('logs', host="staff", args=(self.deletion_context.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_logs_returns_404_for_nonexisting_logs_pk(self):
        url = reverse('logs', host="staff", args=(self.deletion_context.id + 100,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_author_color_is_set_in_response(self):
        url = reverse('logs', host="staff", args=(self.deletion_context.id,))
        response = self.client.get(url)
        role_colour = hex_colour(self.developers_role.colour)
        html_needle = (
            f'<span class="discord-username" style="color: {role_colour}">{self.author}</span>'
        )
        self.assertInHTML(html_needle, response.content.decode())
