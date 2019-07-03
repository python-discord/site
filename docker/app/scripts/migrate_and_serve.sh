#!/bin/sh -eu

### NOTE
# This file is intended to be used by local setups.
# You do not want to run the Django development server
# in production. The default Dockerfile command will
# run using uWSGI, this script is provided purely as
# a convenience to run migrations and start a development server.

echo [i] Applying migrations.
python manage.py migrate --verbosity 1

echo [i] Collecting static files.
python manage.py collectstatic --no-input --clear --verbosity 1

echo [i] Creating a superuser.
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin', 'admin') if not User.objects.filter(username='admin').exists() else print('Admin user already exists')" | python manage.py shell

echo [i] Starting server.
python manage.py runserver 0.0.0.0:8000
