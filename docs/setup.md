# Setup

Setting up the Python site for local development
is quick and easy using `pip`.
Alternatively, you can set it up using Docker.
Both of these methods are documented here.

## PostgreSQL setup

Install PostgreSQL according to its documentation.
Then, create databases and users:

```sql
$ psql -qd postgres
postgres=# CREATE USER pysite WITH CREATEDB;
postgres=# CREATE DATABASE pysite OWNER pysite;
```

Using different databases for development
and tests is recommended because Django
will expect an empty database when running tests.
Now that PostgreSQL is set up, simply set the proper database URL
in your environment variables:

```sh
export DATABASE_URL=postgres://pysite@localhost/pysite
```

After this step, inside the `.env` file, set the `SECRET_KEY` variable which can be anything you like.

A simpler approach to automatically configuring this might come in the
near future - if you have any suggestions, please let us know!

## Development with Docker

To quickly set up the site locally, you can use Docker.
You will need Docker itself and `docker-compose` -
you can omit the latter if you want to use PostgreSQL on
your host. Refer to the docker documentation on how to install Docker.

If you want to set the site up using `docker-compose`, simply run

```sh
docker-compose up
```

and it will do its magic.

Otherwise, you need to set a bunch of environment variables (or pass them along to
the container). You will also need to have a running PostgreSQL instance if you want
to run on your host's PostgreSQL instance.

## Development with `pip`

This is the recommended way if you wish to quickly test your changes and don't want
the overhead that Docker brings.

Follow the PostgreSQL setup instructions above. Then, create a virtual environment
for the project. If you're new to this, you may want to check out [Installing packages
using pip and virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)
from the Python Packaging User Guide.

Enter the virtual environment. Now you can run

```sh
pip install -e .[lint,test]
```

to install base dependencies along with lint and test dependencies.

To run tests, use `python manage.py test`.

## Hosts file

Make sure you add the following to your hosts file:

```sh
127.0.0.1   pythondiscord.local
127.0.0.1   api.pythondiscord.local
127.0.0.1   staff.pythondiscord.local
127.0.0.1   admin.pythondiscord.local
127.0.0.1   wiki.pythondiscord.local
127.0.0.1   ws.pythondiscord.local
```
When trying to access the site, you'll be using the domains above instead of the usual `localhost:8000`.

Finally, you will need to set the environment variable `DEBUG=1`. When using `pipenv`, you can
set put this into an `.env` file to have it exported automatically. It's also recommended to
export `LOG_LEVEL=INFO` when using `DEBUG=1` if you don't want super verbose logs.

To run the server, run `python manage.py runserver`. If it gives you an error saying
`django.core.exceptions.ImproperlyConfigured: Set the DATABASE_URL environment variable` please make sure the server that your postgres database is located at is running
and run the command `$(export cat .env)`. Happy hacking!
