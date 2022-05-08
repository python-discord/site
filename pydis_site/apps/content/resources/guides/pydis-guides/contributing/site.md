---
title: Contributing to Site
description: A guide to setting up and configuring Site.
icon: fab fa-github
toc: 1
---

# Requirements

- [Python 3.9](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
    - `pip install poetry`
- [Git](https://git-scm.com/downloads)
    - [Windows](https://git-scm.com/download/win)
    - [MacOS](https://git-scm.com/download/mac) or `brew install git`
    - [Linux](https://git-scm.com/download/linux)

Using Docker (recommended):

- [Docker CE](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
    - `pip install docker-compose`

Without Docker:

- [PostgreSQL](https://www.postgresql.org/download/)
    - Note that if you wish, the webserver can run on the host and still use Docker for PostgreSQL.

---
# Development environment

1. [Clone your fork to a local project directory](../cloning-repository/)
2. [Install the project's dependencies](../installing-project-dependencies/)

## Without Docker

Some additional steps are needed when not using Docker. Docker abstracts away these steps which is why using it is generally recommended.

### 1. PostgreSQL setup

Enter psql, a terminal-based front-end to PostgreSQL:

```shell
psql -qd postgres
```

Run the following queries to create the user and database:

```sql
CREATE USER pysite WITH SUPERUSER PASSWORD 'pysite';
CREATE DATABASE pysite WITH OWNER pysite;
CREATE DATABASE metricity WITH OWNER pysite;
```

Finally, enter `/q` to exit psql.

### 2. Environment variables

These contain various settings used by the website. To learn how to set environment variables, read [this page](../configure-environment-variables/) first.

```shell
DATABASE_URL=postgres://pysite:pysite@localhost:7777/pysite
METRICITY_DB_URL=postgres://pysite:pysite@localhost:7777/metricity
DEBUG=1
SECRET_KEY=suitable-for-development-only
STATIC_ROOT=staticfiles
```

The [Configuration in Detail](#configuration-in-detail) section contains
detailed information about these settings.

#### Notes regarding `DATABASE_URL`

- If the database is hosted locally i.e. on the same machine as the webserver, then use `localhost` for the host. Windows and macOS users may need to use the [Docker host IP](https://stackoverflow.com/questions/22944631/how-to-get-the-ip-address-of-the-docker-host-from-inside-a-docker-container) instead.
- If the database is running in Docker, use port `7777`. Otherwise, use `5432` as that is the default port used by PostegreSQL.
- If you configured PostgreSQL in a different manner or you are not hosting it locally, then you will need to determine the correct host and port yourself.
The user, password, and database name should all still be `pysite` unless you deviated from the setup instructions in the previous section.

---
# Run the project

The project can be started with Docker or by running it directly on your system.

## Run with Docker

Start the containers using Docker Compose:

```shell
docker-compose up
```

The `-d` option can be appended to the command to run in detached mode. This runs the containers in the background so the current terminal session is available for use with other things.

If you get any Docker related errors, reference the [Possible Issues](https://pythondiscord.com/pages/contributing/docker/#possible-issues") section of the Docker page.
{: .notification .is-warning }

## Run on the host

Running on the host is particularly useful if you wish to debug the site. The [environment variables](#2-environment-variables) shown in a previous section need to have been configured.

### Database

First, start the PostgreSQL database.
Note that this can still be done with Docker even if the webserver will be running on the host - simply adjust the `DATABASE_URL` environment variable accordingly.

If you chose to use Docker for just the database, use Docker Compose to start the container:

```shell
docker-compose up postgres
```

If you're not using Docker, then use [pg_ctl](https://www.postgresql.org/docs/current/app-pg-ctl.html) or your system's service manager if PostgreSQL isn't already running.

### Webserver

Starting the webserver is done simply through poetry:

```shell
poetry run task start
```

---
# Working on the project

The development environment will watch for code changes in your project directory and will restart the server when a module has been edited automatically.
Unless you are editing the Dockerfile or docker-compose.yml, you shouldn't need to manually restart the container during a developing session.

[**Click here to see the basic Git workflow when contributing to one of our projects.**](../working-with-git/)

---
# Django admin site

Django provides an interface for administration with which you can view and edit the models among other things.

It can be found at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/). The default credentials are `admin` for the username and `admin` for the password.

---

# Configuration in detail

The website is configured through the following environment variables:

## Essential
- **`DATABASE_URL`**: A string specifying the PostgreSQL database to connect to,
  in the form `postgresql://user:password@host/database`, such as
  `postgresql://joethedestroyer:ihavemnesia33@localhost/pysite_dev`

- **`METRICITY_DB_URL`**: A string specifying the PostgreSQL metric database to
 connect to, in the same form as `$DATABASE_URL`.

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

- **`STATIC_ROOT`**: The root in which `python manage.py collectstatic`
  collects static files. Optional, defaults to `/app/staticfiles` for the
  standard Docker deployment.

---

# Next steps
Now that you have everything setup, it is finally time to make changes to the site! If you have not yet read the [contributing guidelines](../contributing-guidelines.md), now is a good time. Contributions that do not adhere to the guidelines may be rejected.

If you're not sure where to go from here, our [detailed walkthrough](../#2-set-up-the-project) is for you.

Have fun!
