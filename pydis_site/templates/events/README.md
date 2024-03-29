# Events pages

## Homepage (`index.html`)

The main events page showcases current, upcoming and recent events, as well as
a gallery of the regular events and ad-hoc events we run.

- **Current event** (`current_event.html`)

  This file should be updated when the previous 'current' event has finished
  and there is an upcoming event to promote. It should include some branding
  assets either as a banner, icon, or both for this event.

- **Scheduled events** (`scheduled_events.html`)

  A list of events with brief descriptions each paired with an icon that is
  scheduled to happen strictly after the current date. The list is
  chronological and the first item can be the same as that of "Current event".

  This file should be updated when a new event is scheduled or the top event
  from the list has finished.

### Sidebars

- **Previous events** (`sidebar/main_sidebar.html`)

  Concise list of events for returning members to quickly access after events
  have finished.

  This file should be updated whenever another event has finished.


### Main events (`main_events.html`)

A gallery of events we run regularly — most likely at least once a year. The
descriptions in each card are longer and more detailed.

This file should be updated when we want to reorder the list or add/remove
regular events.

If the total visual height of the entire gallery is modified, please also
update the [CSS file](../../static/css/events/base.css) to set the correct new
height on mobile, tablets, and desktop. This ensures the responsive Masonry
layout displays correctly.


### Other events (`other_events.html`)

A showcase of "ad-hoc" events have we have run in previous years. The list is
not exhausive and is only meant to be a small exhibit for viewers to get a
sense of the kind of events to expect outside of the those regular/annual
events.

This file should be updated when new one-off events that are better deserving
of having a place in the showcase here have been hosted.

Each item should link to a video/article about the event for viewers to
re-watch after the event took place.

Like `main_events.html`, the CSS file should also be updated with the height of
the section changes.
