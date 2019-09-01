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
        self.assertEqual(deletedmessage_filters.hex_colour(Colour.BLACK), "#000000")
        self.assertEqual(deletedmessage_filters.hex_colour(Colour.BLUE), "#0000FF")
        self.assertEqual(deletedmessage_filters.hex_colour(Colour.GREEN), "#00FF00")
        self.assertEqual(deletedmessage_filters.hex_colour(Colour.RED), "#FF0000")
        self.assertEqual(deletedmessage_filters.hex_colour(Colour.WHITE), "#FFFFFF")

    def test_footer_datetime_filter(self):
        datetime_aware = timezone.now()
        iso_string = datetime_aware.isoformat()

        datetime_returned = deletedmessage_filters.footer_datetime(iso_string)
        self.assertTrue(timezone.is_aware(datetime_returned))
        self.assertEqual(datetime_aware, datetime_returned)
