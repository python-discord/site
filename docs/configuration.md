# Configuration
The website is configured through the following environment variables:

## Essential
- **`DATABASE_URL`**: A string specifying the PostgreSQL database to connect to,
  in the form `postgresql://user:password@host/database`, such as
  `postgresql://joethedestroyer:ihavemnesia33@localhost/pysite_dev`

- **`DEBUG`**: Controls Django's internal debugging setup. Enable this when
  you're developing locally. Optional, defaults to `False`.

- **`LOG_LEVEL`**: Any valid Python `logging` module log level - one of `DEBUG`,
  `INFO`, `WARN`, `ERROR` or `CRITICAL`. When using debug mode, this defaults to
  `INFO`. When testing, defaults to `ERROR`. Otherwise, defaults to `WARN`.

## Deployment
- **`ALLOWED_HOSTS`**: A comma-separated lists of alternative hosts to allow to
  host the website on, when `DEBUG` is not set. Optional, defaults to the
  `pythondiscord.com` family of domains.

- **`SECRET_KEY`**: The secret key used in various parts of Django. Keep this
  secret as the name suggests! This is managed for you in debug setups.

- **`STATIC_ROOT`**: The root in which `python manage.py collectstatic` collects
  static files. Optional, defaults to `/var/www/pythondiscord.com`.
