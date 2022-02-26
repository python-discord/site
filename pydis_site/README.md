# `pydis_site` project directory

This directory hosts the root of our **Django project**[^1], and is responsible
for all logic powering our website. Let's go over the directories in detail:

- [`apps`](./apps) contains our **Django apps**. If you want to add your own
  API endpoint or new functionality to our homepage, that's the place to go.
  Each individual application also has its own README.md that you can click
  through.

- [`static`](./static) contains our **static files**, such as CSS, JavaScript,
  images, and anything else that isn't either content or Python code. Static
  files relevant for a specific application are put into subdirectories named
  after the application.

- [`templates`](./templates) contains our **Django templates**. Like with static
  files, templates specific to a single application are stored in a subdirectory
  named after that application. We also have two special templates here:

  - `404.html`, which is our error page shown when a site was not found.

  - `500.html`, which is our error page shown in the astronomically rare case
    that we encounter an internal server error.



Note that for both `static` and `templates`, we are not using the default Django
directory structure which puts these directories in a directory per app (in our
case, this would for example be ``pydis_site/apps/content/static/``).

We also have a few files in here that are relevant or useful in large parts of
the website:

- [`context_processors.py`](./context_processors.py), which contains custom
  *context processors* that add variables to the Django template context. To
  read more, see the [`RequestContext` documentation from
  Django](https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.RequestContext)

- [`settings.py`](./settings.py), our Django settings file. This mostly just
  parses configuration out of your environment variables, so you shouldn't need
  to edit it directly unless you want to add new settings.

- [`urls.py`](./urls.py), which configures our Django URL routing by installing
  our apps into the routing tree.

- [`wsgi.py`](./wsgi.py), which serves as an adapter for
  [`gunicorn`](https://github.com/benoitc/gunicorn),
  [`uwsgi`](https://github.com/unbit/uwsgi) or other application servers to run
  our application in production. Unless you want to test an interaction between
  our application and those servers, you probably won't need to touch this.


[^1]: See [Django Glossary: project](https://docs.djangoproject.com/en/dev/glossary/#term-project)
