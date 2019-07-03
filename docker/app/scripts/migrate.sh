#!/usr/bin/env bash

echo --- Applying migrations ---
python manage.py migrate --verbosity 2

echo --- Collecting static files ---
python manage.py collectstatic --no-input --clear --verbosity 2

echo --- Starting uwsgi ---
exec "$@"  # This runs the CMD at the end of the Dockerfile
