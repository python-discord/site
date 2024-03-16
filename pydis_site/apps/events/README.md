# The "events" app

This application serves mostly static pages that showcase events we run on our
community. You most likely want to look at the [templates
directory](../../templates/events) for this app if you want to change anything.

## Directory structure

This app has a relatively minimal structure:

- `migrations` is empty as we don't work with any models here.

- `tests` contains a few tests to make sure that serving our events pages works.

- `views` contains Django views that concern themselves with looking up the
  matching Django template.

The actual content lives in the [templates directory two layers
up](../../templates/events). Read the
[README.md](../../templates/events/README.md) in that directory for more
details.
