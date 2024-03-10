# The "resources" app

This Django application powering the resources list [on our
website](https://www.pythondiscord.com/resources/).

The main point of interest here lies in the `resources` directory: every
`.yaml` file in here represents a resource that is listed on our website. If
you are looking for the place to add new resources, said directory is the
place to create a new YAML file.

In regards to the required keys and our values, it's best to check the other
files we have for a reference.

Here are some general guidelines:

- The `description` text can include HTML elements, such as a simple bullet-list
  to further describe the resource item. Markdown is not yet supported.

- If branding icons (like Goodreads or GitHub through the `icon` field under
  `urls`) are included, set `color: dark` rather than `color: black` to ensure it
  displays correctly in dark mode.

- For books, please include a link to the Goodreads URL under `urls`.

- If a logo is included, use `icon_image` rather than `title_image` to have the
  logo display together next to the title (rather than replacing it). Unless
  the logo includes the name of the resources that is clearly visible.

- All images used must be readable in both light and dark modes. If an image does
  not suit both themes simultaneously, please include image URLs for each mode
  separately using the optional `*_dark` keys:
  - `icon_image`, `icon_image_dark`
  - `title_image`, `title_image_dark`
  - `title_icon`, `title_icon_dark`


## Directory structure

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
