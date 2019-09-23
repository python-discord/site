FROM python:3.7
RUN pip --no-cache-dir wheel --wheel-dir=/wheels "wiki @ git+https://github.com/python-discord/django-wiki.git"
