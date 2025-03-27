import datetime

from django.utils import timezone


def is_stale(last_update: datetime.datetime, expire_seconds: int) -> bool:
    """Check if the given timestamp is stale, if it is considered expired after `expire_seconds` seconds."""
    return (timezone.now() - last_update).total_seconds() > expire_seconds
