import enum

from django.test import TestCase
from django.utils import timezone

from ..templatetags import deletedmessage_filters


class Colour(enum.IntEnum):
    """Enumeration of integer colour values for readability."""

    BLACK = 0
    BLUE = 255
    GREEN = 65280
    RED = 16711680
    WHITE = 16777215


class DeletedMessageFilterTests(TestCase):
    def test_hex_colour_filter(self):
        """The filter should produce the correct hex values from the integer representations."""
        test_values = (
            (Colour.BLUE, "#0000FF"),
            (Colour.GREEN, "#00FF00"),
            (Colour.RED, "#FF0000"),
            (Colour.WHITE, "#FFFFFF"),

            # Since we're using a "Discord dark theme"-like front-end, show black text as white.
            (Colour.BLACK, "#FFFFFF"),
        )

        for colour, hex_value in test_values:
            with self.subTest(colour=colour, hex_value=hex_value):
                self.assertEqual(deletedmessage_filters.hex_colour(colour), hex_value)

    def test_footer_datetime_filter(self):
        """The filter should parse the ISO-datetime string and return a timezone-aware datetime."""
        datetime_aware = timezone.now()
        iso_string = datetime_aware.isoformat()

        datetime_returned = deletedmessage_filters.footer_datetime(iso_string)
        self.assertTrue(timezone.is_aware(datetime_returned))
        self.assertEqual(datetime_aware, datetime_returned)

    def test_visual_newlines_filter(self):
        """The filter should replace newline characters by newline character and html linebreak."""
        html_br = " <span class='has-text-grey'>↵</span><br>"

        test_values = (
            (
                "Hello, this line does not contain a linebreak",
                "Hello, this line does not contain a linebreak"
            ),
            (
                "A single linebreak\nin a string",
                f"A single linebreak{html_br}in a string"
            ),
            (
                "Consecutive linebreaks\n\n\nwork, too",
                f"Consecutive linebreaks{html_br}{html_br}{html_br}work, too"
            )
        )

        for input_, expected_output in test_values:
            with self.subTest(input=input_, expected_output=expected_output):
                self.assertEqual(deletedmessage_filters.visible_newlines(input_), expected_output)
