import datetime

from django.utils import timezone


def is_stale(last_update: datetime.datetime, expire_seconds: int) -> bool:
    return (timezone.now() - last_update).total_seconds() > expire_seconds
