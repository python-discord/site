# The "home" app

This Django application takes care of serving the homepage of our website, that
is, the first page that you see when you open pythondiscord.com.

## Directory structure

- `migrations` is the standard Django migrations folder. As with [the API
  app](../api/README.md), you usually won't need to edit this manually, use
  `python manage.py makemigrations [-n short_description]` to create a new
  migration here.

- `templatetags` contains custom [template tags and
  filters](https://docs.djangoproject.com/en/dev/howto/custom-template-tags/)
  used in the home app.

- `tests` contains unit tests that validate the home app works as expected. If
  you're looking for guidance in writing tests, the [Django tutorial
  introducing automated
  testing](https://docs.djangoproject.com/en/dev/intro/tutorial05/) is a great
  starting point.

As for the Python modules residing directly in here:

- `models.py` contains our Django model definitions for this app. As this app
  is rather minimal, this is kept as a single module - more models would be
  split up into a subfolder as in the other apps.

- `urls.py` configures Django's [URL
  dispatcher](https://docs.djangoproject.com/en/dev/topics/http/urls/) for our
  home endpoints.

- `views.py` contains our Django views. You can see where they are linked in the
  URL dispatcher.
