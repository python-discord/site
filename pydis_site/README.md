# `pydis_site` project directory

This directory hosts the root of our **Django project**[^1], and is responsible
for all logic powering our website. Let's go over the directories in detail:

- [`apps`](./apps) contains our **Django apps**, which are the building blocks
  that make up our Django project. A Django project must always consist of one
  or more apps, and these apps can be made completely modular and reusable
  across any Django project. In our project, each app controls a distinct part
  of our website, such as the API or our resources system.

  For more information on reusable apps, see the official Django tutorial,
  [which has a section on reusable
  apps](https://docs.djangoproject.com/en/dev/intro/reusable-apps/). To learn
  more about our specific apps, see the README inside the app folder itself.

- [`static`](./static) contains our **static files**, such as CSS, JavaScript,
  images, and anything else that isn't either content or Python code. Static
  files relevant for a specific application are put into subdirectories named
  after the application.

- [`templates`](./templates) contains our **[Django
  templates](https://docs.djangoproject.com/en/dev/topics/templates/)**. Like
  with static files, templates specific to a single application are stored in a
  subdirectory named after that application. We also have two special templates
  here:

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

- [`settings.py`](./settings.py), our Django settings file. This controls all
  manner of crucial things, for instance, we use it to configure logging, our
  connection to the database, which applications are run by the project, which
  middleware we are using, and variables for `django-simple-bulma` (which
  determines frontend colours & extensions for our pages).

- [`urls.py`](./urls.py), the URL configuration for the project itself. Here we
  can forward certain URL paths to our different apps, which have their own
  `urls.py` files to configure where their subpaths will lead. These files
  determine _which URLs will lead to which Django views_.

- [`wsgi.py`](./wsgi.py), which serves as an adapter for
  [`gunicorn`](https://github.com/benoitc/gunicorn),
  [`uwsgi`](https://github.com/unbit/uwsgi), or other application servers to run
  our application in production. Unless you want to test an interaction between
  our application and those servers, you probably won't need to touch this.


[^1]: See [Django Glossary: project](https://docs.djangoproject.com/en/dev/glossary/#term-project)
