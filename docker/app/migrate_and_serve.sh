#!/bin/sh

### NOTE
# This file is intended to be used by local setups.
# You do not want to run the Django development server
# in production. The default Dockerfile command will
# run using uWSGI, this script is provided purely as
# a convenience to run migrations and start a development server.

echo [i] Applying migrations.
python manage.py migrate --verbosity 0
echo [i] Collecting static files.
python manage.py collectstatic --no-input --clear --verbosity 0
echo [i] Starting server.
python manage.py runserver 0.0.0.0:8000
