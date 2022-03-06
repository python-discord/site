# The "api" app

This application takes care of most of the heavy lifting in the site, that is,
allowing our bot to manipulate and query information stored in the site's
database.

We make heavy use of [Django REST
Framework](https://www.django-rest-framework.org) here, which builds on top of
Django to allow us to easily build out the
[REST](https://en.wikipedia.org/wiki/Representational_state_transfer) API
consumed by our bot. Working with the API app requires basic knowledge of DRF -
the [quickstart
guide](https://www.django-rest-framework.org/tutorial/quickstart/) is a great
resource to get started.

## Directory structure

Let's look over each of the subdirectories here:

- `migrations` is the standard Django migrations folder. You usually won't need
  to edit this manually, as `python manage.py makemigrations` handles this for
  you in case you change our models. (Note that when generating migrations and
  Django doesn't generate a human-readable name for you, please supply one
  manually using `-n add_this_field`.)

- `models` contains our Django model definitions. We put models into subfolders
  relevant as to where they are used - in our case, the `bot` folder contains
  models used by our bot when working with the API. Each model is contained
  within its own module, such as `api/models/bot/message_deletion_context.py`,
  which contains the `MessageDeletionContext` model.

- `tests` contains tests for our API. If you're unfamilar with Django testing,
  the [Django tutorial introducing automated
  testing](https://docs.djangoproject.com/en/dev/intro/tutorial05/) is a great
  resource, and you can also check out code in there to see how we test it.

- `viewsets` contains our [DRF
  viewsets](https://www.django-rest-framework.org/api-guide/viewsets/), and is
  structured similarly to the `models` folder: The `bot` subfolder contains
  viewsets relevant to the Python Bot, and each viewset is contained within its
  own module.

The remaining modules mostly do what their name suggests:

- `admin.py`, which hooks up our models to the [Django admin
  site](https://docs.djangoproject.com/en/dev/ref/contrib/admin/).

- `apps.py` contains the Django [application
  config](https://docs.djangoproject.com/en/dev/ref/applications/) for the `api`
  app, and is used to run any code that should run when the app is loaded.

- `pagination.py` contains custom
  [paginators](https://www.django-rest-framework.org/api-guide/pagination/) used
  within our DRF viewsets.

- `serializers.py` contains [DRF
  serializers](https://www.django-rest-framework.org/api-guide/serializers/) for
  our models, and also includes validation logic for the models.

- `signals.py` contains [Django
  Signals](https://docs.djangoproject.com/en/dev/topics/signals/) for running
  custom functionality in response to events such as deletion of a model
  instance.

- `urls.py` configures Django's [URL
  dispatcher](https://docs.djangoproject.com/en/dev/topics/http/urls/) for our
  API endpoints.

- `views.py` is for any standard Django views that don't make sense to be put
  into DRF viewsets as they provide static data or other functionality that
  doesn't interact with our models.
