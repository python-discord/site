---
title: Contributing to Sir Lancebot
description: A guide to setting up and configuring Sir Lancebot.
icon: fab fa-github
toc: 1
---

> Before contributing, please ensure you read the [contributing guidelines](../contributing-guidelines) in full.

---
# Requirements
- [Python 3.9](https://www.python.org/downloads/)
- [Poetry](https://github.com/python-poetry/poetry#installation)
- [Git](https://git-scm.com/downloads)
    - [Windows Installer](https://git-scm.com/download/win)
    - [MacOS Installer](https://git-scm.com/download/mac) or `brew install git`
    - [Linux](https://git-scm.com/download/linux)

## Using Gitpod
Sir Lancebot can be edited and tested on Gitpod. Gitpod will automatically install the correct dependencies and Python version, so you can get straight to coding.
To do this, you will need a Gitpod account, which you can get [here](https://www.gitpod.io/#get-started). Afterwards, either click the button on Sir Lancebot's README or go to https://gitpod.io/#/python-discord/sir-lancebot and run the following commands in the terminal: 
```sh
git remote rename origin upstream
git add remote origin https://github.com/{your_username}/sir-lancebot
```
This will swap the Python Discord origin to upstream and add your own repository as the origin. Once you add your environment variables, you're ready to start contributing.

## Using Docker
Sir Lancebot can be started using Docker. Using Docker is generally recommended (but not strictly required) because it abstracts away some additional set up work.

The requirements for Docker are:

* [Docker CE](https://docs.docker.com/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)
    * `pip install docker-compose`
    * This is only a required step for linux. Docker comes bundled with docker-compose on Mac OS and Windows.

---

# Fork the Project
You will need your own remote (online) copy of the project repository, known as a *fork*.

- [**Learn how to create a fork of the repository here.**](../forking-repository)

You will do all your work in the fork rather than directly in the main repository.

---

# Development Environment
1. Once you have your fork, you will need to [**clone the repository to your computer**](../cloning-repository).
2. After cloning, proceed to [**install the project's dependencies**](../installing-project-dependencies). (This is not required if using Docker)

---
# Test Server and Bot Account

You will need your own test server and bot account on Discord to test your changes to the bot.

1. [**Create a test server**](../setting-test-server-and-bot-account#setting-up-a-test-server).
2. [**Create a bot account**](../setting-test-server-and-bot-account#setting-up-a-bot-account) and invite it to the server you just created.
3. Create the following text channels:
    * `#announcements`
    * `#dev-log`
    * `#sir-lancebot-commands`
4. Create the following roles:
    * `@Admin`
5. Note down the IDs for your server, as well as any channels and roles created.
    * [**Learn how to obtain the ID of a server, channel or role here.**](../setting-test-server-and-bot-account#obtain-the-ids)

---

## Environment variables
You will have to setup environment variables:

* [**Learn how to set environment variables here.**](../configure-environment-variables)

The following variables are needed for running Sir Lancebot:

| Environment Variable | Description |
| -------- | -------- |
| `BOT_TOKEN` | Bot Token from the [Discord developer portal](https://discord.com/developers/applications) |
| `BOT_GUILD` | ID of the Discord Server |
| `BOT_ADMIN_ROLE_ID` | ID of the role `@Admins` |
| `ROLE_HELPERS` | ID of the role `@Helpers` |
| `CHANNEL_ANNOUNCEMENTS` | ID of the `#announcements` channel |
| `CHANNEL_DEVLOG` | ID of the `#dev-log` channel |
| `CHANNEL_COMMUNITY_BOT_COMMANDS` | ID of the `#sir-lancebot-commands` channel |

[**Full environment variable reference for this project.**](./env-var-reference)

---

While not required, we advise you set `USE_FAKEREDIS` to `true` in development to avoid the need of setting up a Redis server.
It does mean you may lose persistent data on restart but this is non-critical.
Otherwise, please see the below linked guide for Redis related variables.
{: .notification .is-warning }

---
# Run the project
The sections below describe the two ways you can run this project. We recomend Docker as it requires less setup.

## Run with Docker
Make sure to have Docker running, then use the Docker command `docker-compose up` in the project root.
The first time you run this command, it may take a few minutes while Docker downloads and installs Sir Lancebot's dependencies.

```shell
$ docker-compose up
```

If you get any Docker related errors, reference the [Possible Issues](../docker#possible-issues) section of the Docker page.
{: .notification .is-warning }

## Run on the host
After installing project dependencies use the poetry command `poetry run task start` in the project root.

```shell
$ poetry run task start
```

---

# Working with Git
Now that you have everything setup, it is finally time to make changes to the bot! If you have not yet [read the contributing guidelines](https://github.com/python-discord/sir-lancebot/blob/main/CONTRIBUTING.md), now is a good time. Contributions that do not adhere to the guidelines may be rejected.

Notably, version control of our projects is done using Git and Github. It can be intimidating at first, so feel free to ask for any help in the server.

[**Click here to see the basic Git workflow when contributing to one of our projects.**](../working-with-git/)

Have fun!
