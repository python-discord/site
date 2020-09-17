from django.test import Client, TestCase
from django.utils import timezone
from django_hosts.resolvers import reverse, reverse_host

from pydis_site.apps.api.models.bot import DeletedMessage, MessageDeletionContext, Role, User
from pydis_site.apps.staff.templatetags.deletedmessage_filters import hex_colour


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
        )

        cls.author.roles.append(cls.developers_role.id)

        cls.deletion_context = MessageDeletionContext.objects.create(
            actor=cls.actor,
            creation=timezone.now()
        )

        cls.deleted_message_one = DeletedMessage.objects.create(
            author=cls.author,
            id=614125807161573397,
            channel_id=1984,
            content='<em>I think my tape has run out...</em>',
            embeds=[],
            attachments=[],
            deletion_context=cls.deletion_context,
        )

        cls.embed_one = {
            "footer": {
                "text": "This will be displayed in the footer!",
                "icon_url": "https://avatars0.githubusercontent.com/u/33516116?s=460&v=4"
            },
            "image": {
                "url": "https://avatars0.githubusercontent.com/u/33516116?s=460&v=4"
            },
            "thumbnail": {
                "url": "https://avatars0.githubusercontent.com/u/33516116?s=460&v=4"
            },
            "author": {
                "name": "Ves Zappa",
                "url": "https://pydis.com",
                "icon_url": "https://avatars0.githubusercontent.com/u/33516116?s=460&v=4"
            },
            "fields": [
                {
                    "inline": False,
                    "name": "Field Name 1",
                    "value": "Field Value 1"
                },
                {
                    "inline": False,
                    "name": "Field Name 2",
                    "value": "Field Value 2"
                },
                {
                    "inline": True,
                    "name": "Field Name 3",
                    "value": "Field Value 3"
                },
                {
                    "inline": True,
                    "name": "Field Name 4",
                    "value": "Field Value 4"
                },
                {
                    "inline": True,
                    "name": "Field Name 5",
                    "value": "Field Value 5"
                }
            ],
            "color": 16711680,
            "timestamp": "2019-08-21T13:58:34.480053+00:00",
            "type": "rich",
            "description": "This embed is way too cool to be seen in public channels.",
            "url": "https://pythondiscord.com/",
            "title": "Hello, PyDis"
        }

        cls.embed_two = {
            "description": "This embed is way too cool to be seen in public channels.",
        }

        cls.deleted_message_two = DeletedMessage.objects.create(
            author=cls.author,
            id=614444836291870750,
            channel_id=1984,
            content='Does that mean this thing will halt?',
            embeds=[cls.embed_one, cls.embed_two],
            attachments=['https://http.cat/100', 'https://http.cat/402'],
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

    def test_correct_messages_have_been_passed_to_template(self):
        url = reverse('logs', host="staff", args=(self.deletion_context.id,))
        response = self.client.get(url)
        self.assertIn("messages", response.context)
        self.assertListEqual(
            [self.deleted_message_two, self.deleted_message_one],
            list(response.context["deletion_context"].deletedmessage_set.all())
        )

    def test_if_both_embeds_are_included_html_response(self):
        url = reverse('logs', host="staff", args=(self.deletion_context.id,))
        response = self.client.get(url)

        html_response = response.content.decode()
        embed_colour_needle = (
            '<div class="discord-embed-color" style="background-color: {colour}"></div>'
        )
        embed_one_colour = hex_colour(self.embed_one["color"])
        embed_two_colour = "#cacbce"
        self.assertInHTML(embed_colour_needle.format(colour=embed_one_colour), html_response)
        self.assertInHTML(embed_colour_needle.format(colour=embed_two_colour), html_response)

    def test_if_both_attachments_are_included_html_response(self):
        url = reverse('logs', host="staff", args=(self.deletion_context.id,))
        response = self.client.get(url)

        html_response = response.content.decode()
        attachment_needle = '<img alt="Attachment" class="discord-attachment" src="{url}">'
        self.assertInHTML(
            attachment_needle.format(url=self.deleted_message_two.attachments[0]),
            html_response
        )
        self.assertInHTML(
            attachment_needle.format(url=self.deleted_message_two.attachments[1]),
            html_response
        )

    def test_if_html_in_content_is_properly_escaped(self):
        url = reverse('logs', host="staff", args=(self.deletion_context.id,))
        response = self.client.get(url)

        html_response = response.content.decode()
        unescaped_content = "<em>I think my tape has run out...</em>"
        self.assertInHTML(unescaped_content, html_response, count=0)
        escaped_content = "&lt;em&gt;I think my tape has run out...&lt;/em&gt;"
        self.assertInHTML(escaped_content, html_response, count=1)
