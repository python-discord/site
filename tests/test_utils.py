from datetime import datetime, timedelta, timezone

from tests import SiteTest
from pysite.utils.time import is_expired, parse_duration


class DurationParsingTests(SiteTest):
    """Tests the `parse_duration` method provided by `pysite.utils.time`."""

    SIMPLE_DURATION_STRINGS = (
        ('42s', timedelta(seconds=42)),
        ('12m', timedelta(minutes=12)),
        ('20h', timedelta(hours=20)),
        ('7d', timedelta(days=7)),
        ('2w', timedelta(weeks=2))
    )
    COMBINED_DURATION_STRINGS = (
        ('12m30s', timedelta(minutes=12, seconds=30)),
        ('20h5m', timedelta(hours=20, minutes=5)),
        ('7d10h12s', timedelta(days=7, hours=10, seconds=12))
    )

    def test_simple_duration_string_parsing(self):
        for duration_string, added_delta in self.SIMPLE_DURATION_STRINGS:
            timezone_aware_now = datetime.now(timezone.utc)
            self.assertAlmostEqual(
                parse_duration(duration_string).timestamp(),
                (timezone_aware_now + added_delta).timestamp(),
                places=-1  # Being off by < 10 seconds is acceptable
            )

    def test_combined_duration_string_parsing(self):
        for duration_string, added_delta in self.COMBINED_DURATION_STRINGS:
            timezone_aware_now = datetime.now(timezone.utc)
            self.assertAlmostEqual(
                parse_duration(duration_string).timestamp(),
                (timezone_aware_now + added_delta).timestamp(),
                places=-1  # Being off by < 10 seconds is acceptable
            )

    def test_empty_duration_raises_valueerror(self):
        with self.assertRaises(ValueError):
            parse_duration('')

    def test_unknown_char_raises_valueerror(self):
        with self.assertRaises(ValueError):
            parse_duration('12l')

    def test_valid_unit_without_digits_raises_valueerror(self):
        with self.assertRaises(ValueError):
            parse_duration('s')


class ExpiryTests(SiteTest):
    """Tests the `is_expired` method provided by `pysite.utils.time`."""

    EXPIRY_DELTAS = (
        timedelta(seconds=30),
        timedelta(minutes=12),
        timedelta(hours=20),
        timedelta(days=5),
        timedelta(weeks=7)
    )

    def test_datetimes_in_the_past_are_expired(self):
        for delta in self.EXPIRY_DELTAS:
            date = datetime.now(timezone.utc) - delta
            self.assertTrue(is_expired(date))

    def test_datetimes_in_the_future_are_not_expired(self):
        for delta in self.EXPIRY_DELTAS:
            date = datetime.now(timezone.utc) + delta
            self.assertFalse(is_expired(date))
