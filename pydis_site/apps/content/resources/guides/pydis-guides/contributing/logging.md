---
title: Logging
description: Information about logging in our projects.
---

Instead of using `print` statements for logging, we use the built-in [`logging`](https://docs.python.org/3/library/logging.html) module.
Here is an example usage:

```python
import logging

log = logging.getLogger(__name__) # Get a logger bound to the module name.
# This line is usually placed under the import statements at the top of the file.

log.trace("This is a trace log.")
log.warning("BEEP! This is a warning.")
log.critical("It is about to go down!")
```

Print statements should be avoided when possible.
Our projects currently defines logging levels as follows, from lowest to highest severity:

- **TRACE:** These events should be used to provide a *verbose* trace of every step of a complex process. This is essentially the `logging` equivalent of sprinkling `print` statements throughout the code.
- **Note:** This is a PyDis-implemented logging level. It may not be available on every project.
- **DEBUG:** These events should add context to what's happening in a development setup to make it easier to follow what's going while workig on a project. This is in the same vein as **TRACE** logging but at a much lower level of verbosity.
- **INFO:** These events are normal and don't need direct attention but are worth keeping track of in production, like checking which cogs were loaded during a start-up.
- **WARNING:** These events are out of the ordinary and should be fixed, but can cause a failure.
- **ERROR:** These events can cause a failure in a specific part of the application and require urgent attention.
- **CRITICAL:** These events can cause the whole application to fail and require immediate intervention.

Any logging above the **INFO** level will trigger a [Sentry](https://sentry.io) issue and alert the Core Developer team.
