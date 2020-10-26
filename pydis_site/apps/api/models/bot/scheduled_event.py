from collections import namedtuple

from django.core.exceptions import ValidationError
from django.db import models

from .user_event import UserEvent

DATETIME_RANGE = namedtuple("datetime_range", ("start", "end"))


class ScheduledEvent(models.Model):
    """A scheduled user event."""

    user_event = models.OneToOneField(
        UserEvent,
        on_delete=models.CASCADE,
    )
    start_time = models.DateTimeField(
        unique=True,
    )
    end_time = models.DateTimeField(
        unique=True
    )

    def clean(self) -> None:
        """Check for event time overlap and if an organizer has already scheduled an event."""
        # Check if organizer has already scheduled an event
        scheduled_events_by_organizer = ScheduledEvent.objects.filter(
            user_event__organizer=self.user_event.organizer
        )
        if scheduled_events_by_organizer:
            raise ValidationError(
                {
                    "user_event": [
                        f"Organizer {self.user_event.organizer} has already "
                        f"scheduled an event!"
                    ]
                }
            )

        # Check for time overlap
        new_dt_range = DATETIME_RANGE(self.start_time, self.end_time)

        scheduled_events = ScheduledEvent.objects.select_related("user_event").all()

        for event in scheduled_events:
            event_dt_range = DATETIME_RANGE(event.start_time, event.end_time)
            late_start = max(new_dt_range.start, event_dt_range.start)
            early_end = min(new_dt_range.end, event_dt_range.end)

            # 30min should be the minimum time gap between 2 events
            if (late_start - early_end).total_seconds() < 30*60:
                raise ValidationError(
                    {
                        "start_time": [
                            f"Event schedule overlaps with already "
                            f"scheduled event {event.user_event.name}."
                        ]
                    }
                )
