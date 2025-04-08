---
title: Contributing to Sir Lancebot
description: A guide to setting up and configuring Sir Lancebot.
icon: fab fa-github
toc: 1
---

You should have already forked the [`sir-lancebot`](https://github.com/python-discord/sir-lancebot) repository and cloned it to your local machine. If not, check out our [detailed walkthrough](../#1-fork-and-clone-the-repo).

Remember to ensure that you have read the [contributing guidelines](../contributing-guidelines) in full before you start contributing.

### Requirements
- [Python 3.13.*](https://www.python.org/downloads/)
- [Poetry](https://github.com/python-poetry/poetry#installation)
- [Git](https://git-scm.com/downloads)
    - [Windows Installer](https://git-scm.com/download/win)
    - [MacOS Installer](https://git-scm.com/download/mac) or `brew install git`
    - [Linux](https://git-scm.com/download/linux)

---

## Using Gitpod
Sir Lancebot can be edited and tested on Gitpod. Gitpod will automatically install the correct dependencies and Python version, so you can get straight to coding.

To do this, you will need a Gitpod account, which you can get [here](https://www.gitpod.io/#get-started), and a fork of Sir Lancebot. This guide covers forking the repository [here](../forking-repository).

Afterwards, click on [this link](https://gitpod.io/#/github.com/python-discord/sir-lancebot) to spin up a new workspace for Sir Lancebot. Then run the following commands in the terminal after the existing tasks have finished running:
```sh
git remote rename origin upstream
git remote add origin https://github.com/{your_username}/sir-lancebot
```
Make sure you replace `{your_username}` with your Github username. These commands will set the Sir Lancebot repository as the secondary remote, and your fork as the primary remote. This means you can easily grab new changes from the main Sir Lancebot repository.

Once you've set up [a test server and bot account](#test-server-and-bot-account) and your [environment variables](#environment-variables), you are ready to begin contributing to Sir Lancebot!

## Using Docker
Sir Lancebot can be started using Docker. Using Docker is generally recommended (but not strictly required) because it abstracts away some additional set up work.

The requirements for Docker are:

* [Docker CE](https://docs.docker.com/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)
    * `pip install docker-compose`
    * This is only a required step for linux. Docker comes bundled with docker-compose on Mac OS and Windows.

---
# Development Environment
If you aren't using Docker, you will need to [install the project's dependencies](../installing-project-dependencies) yourself.

---
# Test Server and Bot Account

You will need your own test server and bot account on Discord to test your changes to the bot.

1. [**Create a test server**](../setting-test-server-and-bot-account#setting-up-a-test-server).
2. [**Create a bot account**](../setting-test-server-and-bot-account#setting-up-a-bot-account) and invite it to the server you just created.
3. Create the following text channels:
    * `#announcements`
    * `#dev-log`
    * `#sir-lancebot-playground`
4. Create the following roles:
    * `@Admins`
    * `@Helpers`
5. Note down the IDs for your server, as well as any channels and roles created.
    * [**Learn how to obtain the ID of a server, channel or role here.**](../setting-test-server-and-bot-account#obtain-the-ids)

---

## Environment variables
You will have to setup environment variables:

* [**Learn how to set environment variables here.**](../configure-environment-variables)

The following variables are needed for running Sir Lancebot:

| Environment Variable               | Description                                                                                |
|------------------------------------|--------------------------------------------------------------------------------------------|
| `CLIENT_TOKEN`                     | Bot Token from the [Discord developer portal](https://discord.com/developers/applications) |
| `CLIENT_GUILD`                     | ID of the Discord Server                                                                   |
| `ROLES_ADMIN`                      | ID of the role `@Admins`                                                                   |
| `ROLES_HELPERS`                    | ID of the role `@Helpers`                                                                  |
| `CHANNELS_ANNOUNCEMENTS`           | ID of the `#announcements` channel                                                         |
| `CHANNELS_DEVLOG`                  | ID of the `#dev-log` channel                                                               |
| `CHANNELS_SIR_LANCEBOT_PLAYGROUND` | ID of the `#sir-lancebot-playground` channel                                               |

[**Full environment variable reference for this project.**](../sir-lancebot/env-var-reference)

---

While not required, we advise you set `REDIS_USE_FAKEREDIS` to `true` in development to avoid the need of setting up a Redis server.
It does mean you may lose persistent data on restart but this is non-critical.
Otherwise, please see the below linked guide for Redis related variables.
{: .notification .is-warning }

---
# Run the project
The sections below describe the two ways you can run this project. We recommend Docker as it requires less setup.

## Run with Docker
Make sure to have Docker running, then use the Docker command `docker compose up` in the project root.
The first time you run this command, it may take a few minutes while Docker downloads and installs Sir Lancebot's dependencies.

```shell
$ docker compose up
```

If you get any Docker related errors, reference the [Possible Issues](../docker#possible-issues) section of the Docker page.
{: .notification .is-warning }

## Run on the host
After installing project dependencies use the poetry command `poetry run task start` in the project root.

```shell
$ poetry run task start
```
---

# Next steps
Now that you have everything setup, it is finally time to make changes to the bot! If you have not yet read the [contributing guidelines](../contributing-guidelines.md), now is a good time. Contributions that do not adhere to the guidelines may be rejected.

If you're not sure where to go from here, our [detailed walkthrough](../#2-set-up-the-project) is for you.

Have fun!
