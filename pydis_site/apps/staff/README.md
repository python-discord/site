# The "staff" app

This Django application hosts any staff-internal tooling, which, at time of
writing, is only an endpoint to view logs uploaded by the Python bot.

This app mainly interacts with a single model from the `api` app, and has no
models on its own. The following files and directories are of interest:

- [`templatetags`](./templatetags) contains custom template tags that help with
  formatting the HTML templates of this app (these can be found in the template
  root direcetory).

- [`tests`](./tests) contains standard Django unit tests that validate both the
  template tags and functionality of the log viewer itself.

- [`urls.py`](./urls.py) contains the regular Django URL routing logic.

- [`views.py`](./views.py) contains standard Django views. In our case, the
  main work happens in the template, so this is relatively straightforward.
