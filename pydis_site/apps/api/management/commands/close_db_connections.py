from django.core.management.base import BaseCommand
from django.db import connections
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """A command to to close all the open connections to the database."""

    help = "Closes all the open connections to the database"

    def handle(self, *args, **options) -> None:
        """Handle the connection closing command invocation."""
        logger.info("Closing all database connections")
        try:
            connections.close_all()
        except Exception as e:
            logger.exception(e)
