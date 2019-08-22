from django.test import TestCase
from django.utils import timezone

from ..templatetags import deletedmessage_filters


class DeletedMessageFilterTests(TestCase):
    def test_hex_colour_filter(self):
        self.assertEqual(deletedmessage_filters.hex_colour(0), "#000000")
        self.assertEqual(deletedmessage_filters.hex_colour(255), "#0000FF")
        self.assertEqual(deletedmessage_filters.hex_colour(65280), "#00FF00")
        self.assertEqual(deletedmessage_filters.hex_colour(16711680), "#FF0000")
        self.assertEqual(deletedmessage_filters.hex_colour(16777215), "#FFFFFF")

    def test_footer_datetime_filter(self):
        datetime_aware = timezone.now()
        iso_string = datetime_aware.isoformat()

        datetime_returned = deletedmessage_filters.footer_datetime(iso_string)
        self.assertTrue(timezone.is_aware(datetime_returned))
        self.assertEqual(datetime_aware, datetime_returned)
