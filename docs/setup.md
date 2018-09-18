# Setup
Setting up the Python site for local development is quick and easy using `pip`.
Alternatively, you can set it up using Docker. Both of these methods are documented here.

## PostgreSQL setup
Install PostgreSQL according to its documentation. Then, create databases and users:
```sql
$ psql -qd postgres
postgres=# CREATE USER pysite WITH CREATEDB;
postgres=# CREATE DATABASE pysite OWNER pysite;
```
Using different databases for development and tests is recommended because Django
will expect an empty database when running tests.
Now that PostgreSQL is set up, simply set the proper database URL
in your environment variables:
```sh
$ export DATABASE_URL=postgres://pysite@localhost/pysite
```
A simpler approach to automatically configuring this might come in the
near future - if you have any suggestions, please let us know!

## Development with Docker
To quickly set up the site locally, you can use Docker.
You will need Docker itself and `docker-compose` - you can omit the latter if you want to
use PostgreSQL on your host. Refer to the docker documentation on how to install Docker.

If you want to set the site up using `docker-compose`, simply run
```sh
$ docker-compose up
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
$ pip install -e .[lint,test]
```
to install base dependencies along with lint and test dependencies.

You can either use `python manage.py` directly, or you can use the console
entrypoint for it, `psmgr`. For example, to run tests, you could use either
`python manage.py test` or `psmgr test`. Happy hacking!
