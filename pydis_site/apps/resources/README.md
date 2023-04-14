# The "resources" app

This Django application powering the resources list [on our
website](https://www.pythondiscord.com/resources/).

## Directory structure

The main point of interest here lies in the `resources` directory: every
`.yaml` file in here represents a resource that is listed on our website. If
you are looking for the place to suggest new resources, said directory is the
place to create a new YAML file. In regards to the required keys and our
values, it's best to check the other files we have for a reference.

The app has a single view in `views.py` that takes care of reading the `.yaml`
file. This is a standard Django view, mounted in `urls.py` as usual.

Similar to the [home app](../home), the `templatetags` directory contains custom
[template tags and
filters](https://docs.djangoproject.com/en/dev/howto/custom-template-tags/) used
here.

The `tests` directory validates that our redirects and helper functions work as
expected. If you made changes to the app and are looking for guidance on adding
new tests, the [Django tutorial introducing automated
testing](https://docs.djangoproject.com/en/dev/intro/tutorial05/) is a good
place to start.

This application does not use the database and as such does not have models nor
migrations.
