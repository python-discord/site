# The "redirect" app

This Django application manages redirects on our website. The main magic
happens in `urls.py`, which transforms our redirects as configured in
`redirects.yaml` into Django URL routing rules. `tests.py` on the other hand
simply checks that all redirects configured in `redirects.yaml` work as
expected.

As suggested by the comment in `redirects.yaml`, this app is mainly here for
backwards compatibility for our old dewikification project. It is unlikely you
need to edit it directly. If you did find a reason to perform changes here,
please [open an
issue](https://github.com/python-discord/site/issues/new/choose)!
