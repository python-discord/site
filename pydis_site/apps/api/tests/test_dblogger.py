import logging
from datetime import datetime

from django.test import TestCase

from ..dblogger import DatabaseLogHandler
from ..models import LogEntry


class DatabaseLogHandlerTests(TestCase):
    def test_logs_to_database(self):
        logger = logging.getLogger("test_logger")
        logger.handlers = [DatabaseLogHandler()]
        logger.warning("I am a test case!")

        # Ensure we only have a single record in the database
        # after the logging call above.
        [entry] = LogEntry.objects.all()

        self.assertEqual(entry.application, 'site')
        self.assertEqual(entry.logger_name, "test_logger")
        self.assertIsInstance(entry.timestamp, datetime)
        self.assertEqual(entry.level, 'warning')
        self.assertEqual(entry.module, __name__)
        self.assertIsInstance(entry.line, int)
        self.assertEqual(entry.message, "I am a test case!")
