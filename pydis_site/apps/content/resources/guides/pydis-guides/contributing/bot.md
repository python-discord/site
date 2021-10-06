---
title: Contributing to Bot
description: A guide to setting up and configuring Bot.
icon: fab fa-github
toc: 1
---

# Requirements
* [Python 3.9](https://www.python.org/downloads/)
* [Poetry](https://github.com/python-poetry/poetry#installation)
    * `pip install poetry`
* [Git](https://git-scm.com/downloads)
    * [Windows](https://git-scm.com/download/win)
    * [MacOS](https://git-scm.com/download/mac) or `brew install git`
    * [Linux](https://git-scm.com/download/linux)
* A running webserver for the [site](../site)
    * Follow the linked guide only if you don't want to use Docker or if you plan to do development on the site project too.

## Using Docker

Both the site and the bot can be started using Docker.
Using Docker is generally recommended (but not strictly required) because it abstracts away some additional set up work, especially for the site.
However, if you plan to attach a debugger to either the site or the bot, run the respective project directly on your system (AKA the _host_) instead.

The requirements for Docker are:

* [Docker CE](https://docs.docker.com/install/)
* [Docker Compose](https://docs.docker.com/compose/install/) (This already comes bundled on macOS and Windows, so you shouldn't need to install it)
    * `pip install docker-compose`

---
# Fork the project
You will need access to a copy of the git repository of your own that will allow you to edit the code and push your commits to.
Creating a copy of a repository under your own account is called a _fork_.

* [Learn how to create a fork of the repository here.](../forking-repository)

This is where all your changes and commits will be pushed to, and from where your PRs will originate from.

For any staff member, since you have write permissions already to the original repository, you can just create a feature branch to push your commits to instead.

---
# Development environment
1. [Clone your fork to a local project directory](../cloning-repository/)
2. [Install the project's dependencies](../installing-project-dependencies/)

---
# Test server and bot account
You will need your own test server and bot account on Discord to test your changes to the bot.

* [**Create a test server**](../setting-test-server-and-bot-account#setting-up-a-test-server)
* [**Create a bot account**](../setting-test-server-and-bot-account#setting-up-a-bot-account)
* Invite it to the server you just created.

### Privileged Intents

With `discord.py` 1.5 and later, it is now necessary to explicitly request that your Discord bot receives certain gateway events.
The Python bot requires the `Server Member Intent` to function.
In order to enable it, visit the [Developer Portal](https://discord.com/developers/applications/) (from where you copied your bot's login token) and scroll down to the `Privileged Gateway Intents` section.
The `Presence Intent` is not necessary and can be left disabled.

If your bot fails to start with a `PrivilegedIntentsRequired` exception, this indicates that the required intent was not enabled.

### Server Setup

Setup categories, channels, emojis, roles, and webhooks in your server. To see what needs to be added, please refer to the following sections in the `config-default.yml` file:

* `style.emojis`
* `guild.categories`
* `guild.channels`
* `guild.roles`
* `guild.webhooks`

We understand this is tedious and are working on a better solution for setting up test servers.
In the meantime, [here](https://discord.new/zmHtscpYN9E3) is a template for you to use.<br>

---
# Configure the bot
You will need to copy IDs of the test Discord server, as well as the created channels and roles to paste in the config file.
If you're not sure how to do this, [check out the information over here.](../setting-test-server-and-bot-account#obtain-the-ids)

1. Create a copy of `config-default.yml` named `config.yml` in the same directory.
2. Set `guild.id` to your test servers's ID.
3. Change the IDs in the [sections](#server-setup) mentioned earlier to match the ones in your test server.
4. Set `urls.site_schema` and `urls.site_api_schema` to `"http://"`.
5. Set `urls.site`:
    - If running the webserver in Docker, set it to `"web:8000"`.
        - If the site container is running separately (i.e. started from a clone of the site repository), then [COMPOSE_PROJECT_NAME](../docker/#compose-project-names) has to be set to use this domain. If you choose not to set it, the domain in the following step can be used instead.
    - If running the webserver locally and the hosts file has been configured, set it to `"pythondiscord.local:8000"`.
    - Otherwise, use whatever domain corresponds to the server where the site is being hosted.
6. Set `urls.site_api` to whatever value you assigned to `urls.site` with `api` prefixed to it, for example if you set `urls.site` to `web:8000` then set `urls.site_api` to `api.web:8000`.
7. Setup the environment variables listed in the section below.

### Environment variables

These contain various settings used by the bot.
To learn how to set environment variables, read [this page](../configure-environment-variables) first.

The following is a list of all available environment variables used by the bot:

| Variable | Required | Description |
| -------- | -------- | -------- |
| `BOT_TOKEN` | Always | Your Discord bot account's token (see [Test server and bot account](#test-server-and-bot-account)). |
| `BOT_API_KEY` | When running bot without Docker | Used to authenticate with the site's API. When using Docker to run the bot, this is automatically set. By default, the site will always have the API key shown in the example below. |
| `BOT_SENTRY_DSN` | When connecting the bot to sentry | The DSN of the sentry monitor. |
| `BOT_TRACE_LOGGERS ` | When you wish to see specific or all trace logs | Comma separated list that specifies which loggers emit trace logs through the listed names. If the ! prefix is used, all of the loggers except the listed ones are set to the trace level. If * is used, the root logger is set to the trace level. |
| `REDIS_PASSWORD` | When not using FakeRedis | The password to connect to the redis database. *Leave empty if you're not using REDIS.* |

---

If you are running on the host, while not required, we advise you set `use_fakeredis` to `true` in your `config.yml` file during development to avoid the need of setting up a Redis server.
It does mean you may lose persistent data on restart but this is non-critical.
Otherwise, you should set up a Redis instance and fill in the necessary config.
{: .notification .is-warning }

---

Example `.env` file:

```shell
BOT_TOKEN=YourDiscordBotTokenHere
BOT_API_KEY=badbot13m0n8f570f942013fc818f234916ca531
REDDIT_CLIENT_ID=YourRedditClientIDHere
REDDIT_SECRET=YourRedditSecretHere
```

---
# Run the project

The bot can run with or without Docker.
When using Docker, the site, which is a prerequisite, can be automatically set up too.
If you don't use Docker, you have to first follow [the site guide](../site/) to set it up yourself.
The bot and site can be started using independent methods.
For example, the site could run with Docker and the bot could run directly on your system (AKA the _host_) or vice versa.

## Run with Docker

The following sections describe how to start either the site, bot, or both using Docker.
If you are not interested in using Docker, see [this page](../site/) for setting up the site and [this section](#run-on-the-host) for running the bot.

If you get any Docker related errors, reference the [Possible Issues](../docker#possible-issues) section of the Docker page.

### Site and bot

This method will start both the site and the bot using Docker.

Start the containers using Docker Compose while inside the root of the project directory:

```shell
docker-compose up
```

The `-d` option can be appended to the command to run in detached mode.
This runs the containers in the background so the current terminal session is available for use with other things.

### Site only

This method will start only the site using Docker.

```shell
docker-compose up site
```

See [this section](#run-on-the-host) for how to start the bot on the host.

### Bot only

This method will start only the bot using Docker.
The site has to have been started somehow beforehand.

Start the bot using Docker Compose while inside the root of the project directory:

```shell
docker-compose up --no-deps bot
```

## Run on the host

Running on the host is particularly useful if you wish to debug the bot.
The site has to have been started somehow beforehand.

```shell
poetry run task start
```

---
## Working with Git
Now that you have everything setup, it is finally time to make changes to the bot!
If you have not yet [read the contributing guidelines](../contributing-guidelines), now is a good time.
Contributions that do not adhere to the guidelines may be rejected.

Notably, version control of our projects is done using Git and Github.
It can be intimidating at first, so feel free to ask for any help in the server.

[**Click here to see the basic Git workflow when contributing to one of our projects.**](../working-with-git/)

## Adding new statistics

Details on how to add new statistics can be found on the [statistic infrastructure page](https://blog.pythondiscord.com/statistics-infrastructure).
We are always open to more statistics so add as many as you can!

## Running tests

[This section](https://github.com/python-discord/bot/blob/main/tests/README.md#tools) of the README in the `tests` repository will explain how to run tests.
The whole document explains how unittesting works, and how it fits in the context of our project.

Have fun!
