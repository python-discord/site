---
title: Contributing to Bot
description: A guide to setting up and configuring Bot.
icon: fab fa-github
toc: 3
---
The purpose of this guide is to get you a running local version of [the Python bot](https://github.com/python-discord/bot).
You should have already forked the repository and cloned it to your local machine. If not, check out our [detailed walkthrough](../#1-fork-and-clone-the-repo).

This page will focus on the quickest steps one can take, with mentions of alternatives afterwards.

---
## Setting up the project

### Setup Project Dependencies
Below are the dependencies you **must** have installed to get started with the bot.

1. Make sure you have [Python 3.11](https://www.python.org/downloads/) installed. It helps if it is your system's default Python version.
1. [Install Poetry](https://github.com/python-poetry/poetry#installation).
1. [Install the project's dependencies](../installing-project-dependencies).
1. Docker.

<div class="card">
    <button type="button" class="card-header collapsible">
        <span class="card-header-title subtitle is-6 my-2 ml-2">Getting started with Docker</span>
        <span class="card-header-icon">
            <i class="fas fa-fw fa-angle-down title is-5" aria-hidden="true"></i>
        </span>
    </button>
    <div class="collapsible-content collapsed">
        <div class="card-content">
            The requirements for Docker are:
            <ul>
                <li><a href="https://docs.docker.com/install">Docker CE</a></li>
                <li>Docker Compose. If you're using macOS and Windows, this already comes bundled with the previous installation. Otherwise, you can download it either from the <a href="https://docs.docker.com/compose/install">website</a>, or by running <code>pip install docker-compose</code>.</li>
            </ul>
            <p class="notification is-warning">If you get any Docker related errors, reference the <a href="../docker#possible-issues">Possible Issue</a> section of the Docker page.</p>
        </div>
    </div>
</div>
<br>

### Set Up a Test Server
The Python bot is tightly coupled with the Python Discord server, so to have a functional version of the bot you need a server with channels it can use.
It's possible to set the bot to use a single channel for all cogs, but that will cause extreme spam and will be difficult to work with.

You can start your own server and set up channels as you see fit, but for your convenience we have a template for a development server you can use: [https://discord.new/zmHtscpYN9E3](https://discord.new/zmHtscpYN9E3).

Keep in mind that this is not an exact mirror of the Python server, but a reduced version for testing purposes.
The channels there are mostly the ones needed by the bot.
---

### Set Up a Bot Account
You will need your own bot account on Discord to test your changes to the bot.
See [here](../creating-bot-account) for help with setting up a bot account. Once you have a bot account, invite it to the test server you created in the previous section.

#### Privileged Intents

It is necessary to explicitly request that your Discord bot receives certain gateway events.
The Python bot requires the `Server Member Intent` to function.
In order to enable it, visit the [Developer Portal](https://discord.com/developers/applications/) (from where you copied your bot's login token) and scroll down to the `Privileged Gateway Intents` section.
The `Presence Intent` is not necessary and can be left disabled.

If your bot fails to start with a `PrivilegedIntentsRequired` exception, this indicates that the required intent was not enabled.

---

### Configure the Bot
You now have both the bot's code and a server to run it on. It's time for you to connect the two by setting the bot's configuration.

Both `.env` and `.env.server` files we talk about below are ignored by git, so they do not get accidentally commit to the repository.

#### .env
This file will contain sensitive information such as your bot's token, do not share it with anybody!

To start, create a `.env` file in the project root with the below content.

```text
BOT_TOKEN=YourDiscordBotTokenHere
GUILD_ID=YourDiscordTestServerIdHere
BOT_PREFIX=YourDesiredPrefixHere
```
See [here](../creating-bot-account) for help with obtaining the bot token, and [here](../obtaining-discord-ids#guild-id) for help with obtaining the guild's ID.

Other values will be added to your `.env` over time as you need to interact with other parts of the bot, but those are not needed for a basic setup. For a full list of support values see the ENV file option [appendix](#appendix-full-env-file-options)

#### .env.server
All server related configuration values are saved in this file, which also needs to be at the root directory of the project.

We provide a script to automatically generate a server config.  
**Note**: The script **only** works with servers created with the template mentioned above.

If you want to setup the bot from an existing guild read out [manual configuration guide](../bot-extended-configuration-options#manual-constants-configuration). This is far more complicated and time consuming.

Running the below command will use the `BOT_TOKEN` and `GUILD_ID` from the `.env` file you created above to download all of the relevant IDs from the template guild into your `.env.server`

**Note**: This script will overwrite the `.env.server` file. We suggest you put any configuration not generated by this script in to `.env` instead
```shell
$ poetry run task configure
```

Once the script has finished running, you'll notice the creation of a new file called `.env.server` at your project's root directory.
This file will contain the extracted IDs from your server which are necessary for your bot to run.

**Congratulations**, you have finished the configuration and can now [run your bot](#run-it).


<div class="card">
    <button type="button" class="card-header collapsible">
        <span class="card-header-title subtitle is-6 my-2 ml-2">Why do you need a separate config file?</span>
        <span class="card-header-icon">
            <i class="fas fa-fw fa-angle-down title is-5" aria-hidden="true"></i>
        </span>
    </button>
    <div class="collapsible-content collapsed">
        <div class="card-content">
            While it's technically possible to edit the values in <code>constants.py</code> to match your server, it is heavily discouraged.
            This file's purpose is to provide the configurations the Python bot needs to run in the Python server in production, and should remain as such.
            In contrast, the <code>.env.server</code> file can remain in your local copy of the code, and will be ignored by commits via the project's <code>.gitignore</code>.
        </div>
    </div>
</div>
<br>


### Run it!
#### With Docker
You are now almost ready to run the Python bot. The simplest way to do so is with Docker.


With all of the above setup, you can run The projec with `docker compose up`. This will start the bot an all required services! Enter your server and type `!help` (or whatever prefix you chose instead of `!`) to see the bot in action!

Some other useful docker commands are as follows:

1. `docker compose pull` this pulls updates for all non-bot services, such as psotgres, redis and our [site](../site) project!
1. `docker compose build` this rebuilds the bot's docker image, this is only needed if you need to make changes to the bot's dependencies, or the Dockerfile itself.
1. `docker compose --profile 3.10 up` this starts a 3.10 snekbox container, in addition to the default 3.11 container!

Your bot is now running, all inside Docker.

**Note**: If you want to read about how to make debugging with an IDE a easier, or for additional running methods, check out our [extended configuration guide](../bot-extended-configuration-options).

---

## Development Tips
Now that you have everything setup, it is finally time to make changes to the bot!

### Working with Git

Version control of our projects is done using Git and Github.
It can be intimidating at first, so feel free to ask for any help in the server.

[**Click here to see the basic Git workflow when contributing to one of our projects.**](../working-with-git/)

### Running tests

[This section](https://github.com/python-discord/bot/blob/main/tests/README.md#tools) of the README in the `tests` repository will explain how to run tests.
The whole document explains how unittesting works, and how it fits in the context of our project.

Make sure to run tests *before* pushing code.

Even if you run the bot through Docker, you might want to [setup a development environment](../bot-extended-configuration-options#setting-up-a-development-environment) in order to run the tests locally.

### Lint before you push
As mentioned in the [contributing guidelines](../contributing-guidelines), you should make sure your code passes linting for each commit you make.

For ease of development, you can install the pre-commit hook with `poetry run task precommit`, which will check your code every time you try to commit it.
For that purpose, even if you run the bot through Docker, you might want to [setup a development environment](../bot-extended-configuration-options#setting-up-a-development-environment), as otherwise the hook installation will fail.

### Issues?
If you have any issues with setting up the bot, come discuss it with us on the [#dev-contrib](https://discord.gg/2h3qBv8Xaa) channel on our server.

If you find any bugs in the bot or would like to request a feature, feel free to [open an issue](https://github.com/python-discord/bot/issues/new/choose) on the repository.

---

# Next steps
Now that you have everything setup, it is finally time to make changes to the bot! If you have not yet read the [contributing guidelines](../contributing-guidelines.md), now is a good time. Contributions that do not adhere to the guidelines may be rejected.

Have fun!

---

# Appendix: Full ENV File Options
The following is a list of all available environment variables used by the bot:

| Variable             | Required                                          | Description                                                                                                                                                                                                                                         |
|----------------------|---------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `BOT_TOKEN`          | Always                                            | Your Discord bot account's token (see [Set Up a Bot Account](#set-up-a-bot-account)).                                                                                                                                                               |
| `GUILD_ID`           | Always                                            | Your Discord test server's id (see [Set Up a Test Server](#set-up-a-test-server)).                                                                                                                                                                  |
| `BOT_PREFIX`         | When you wish to use a prefix different than "!"  | Your Discord bot command's prefix.                                                                                                                                                                                                                  |
| `API_KEYS_SITE_API`  | When running bot without Docker                   | Used to authenticate with the site's API. When using Docker to run the bot, this is automatically set. By default, the site will always have the API key shown in the example below.                                                                |
| `BOT_SENTRY_DSN`     | When connecting the bot to sentry                 | The DSN of the sentry monitor.                                                                                                                                                                                                                      |
| `BOT_TRACE_LOGGERS ` | When you wish to see specific or all trace logs   | Comma separated list that specifies which loggers emit trace logs through the listed names. If the ! prefix is used, all of the loggers except the listed ones are set to the trace level. If * is used, the root logger is set to the trace level. |
| `DEBUG`              | In production                                     | `true` or `false`, depending on whether to enable debug mode, affecting the behavior of certain features. `true` by default.                                                                                                                        |
| `REDIS_PASSWORD`     | When not using FakeRedis                          | The password to connect to the Redis database (see [Staring Redis with other methods](../bot-extended-configuration-options#starting-redis-using-other-methods)).                                                                                                                                   |
| `USE_METRICITY`      | When using Metricity                              | `true` or `false`, depending on whether to enable metrics collection using Metricity (see [Working with Metricity](../bot-extended-configuration-options#working-with-metricity)). `false` by default.                                                                |
| `API_KEYS_GITHUB`    | When you wish to interact with GitHub             | The API key to interact with GitHub, for example to download files for the branding manager.                                                                                                                                                        |
| `METABASE_USERNAME`  | When you wish to interact with Metabase           | The username for a Metabase admin account.                                                                                                                                                                                                          |
| `METABASE_PASSWORD`  | When you wish to interact with Metabase           | The password for a Metabase admin account.                                                                                                                                                                                                          |
