from datetime import datetime, timezone

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models.bot.bot_setting import validate_bot_setting_name
from ..models.bot.offensive_message import future_date_validator


REQUIRED_KEYS = (
    'content', 'fields', 'image', 'title', 'video'
)


class BotSettingValidatorTests(TestCase):
    def test_accepts_valid_names(self):
        validate_bot_setting_name('defcon')

    def test_rejects_bad_names(self):
        with self.assertRaises(ValidationError):
            validate_bot_setting_name('bad name')


class OffensiveMessageValidatorsTests(TestCase):
    def test_accepts_future_date(self):
        future_date_validator(datetime(3000, 1, 1, tzinfo=timezone.utc))

    def test_rejects_non_future_date(self):
        with self.assertRaises(ValidationError):
            future_date_validator(datetime(1000, 1, 1, tzinfo=timezone.utc))
