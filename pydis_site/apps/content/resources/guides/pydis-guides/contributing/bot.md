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
You now have both the bot's code and a server to run it on. It's time for you to connect the two by changing the bot's configurations.
This can be done either automatically or manually, and we'll be detailing the steps for both.

One thing to know is that the bot relies on precisely **two** configuration files to work

#### .env.server
All server configuration values are saved in this file, which needs to be at the root directory of the cloned code.
This file contains the various configurations we use to make the bot run on the Python Discord server, such as channel and role IDs, and the emojis it works with.
It also contains configurations such as how long it takes for a help channel to time out, and how many messages a user needs to voice-verify.

This file will be created for you automatically if you decide to go with [automatic configuration](#automatic-configuration),
otherwise a lot of it has to be done by hand which will be detailed in the [manual configuration](#manual-configuration) section.

#### .env
This file will mostly contain sensitive information such as your `BOT_TOKEN` and your `REDIS_PASSWORD`.
It will also contain configurations related to external services the bot might use such as `USE_METRICITY`, which are unrelated to your server, with the only exception being `GUILD_ID`.

**Notes**:

* Both `.env` and `.env.server` are and should remain ignored by git, otherwise you risk pushing sensitive information.
* Skip the following step if you would like to configure the bot manually, but that will require more work.

#### Automatic configuration
To make setup much easier, the script in `botstrap.py` bootstraps the configuration for you and helps you get started immediately,
without having to spend much time copying IDs from your server into your configuration file.

**Note**: The script will also work on existing servers as long as the channel names are the same as the one in Python Discord.

##### 1. Script setup
##### 1.1. Environment variables
You will need to create a file called `.env`, which will contain two required values: `BOT_TOKEN` and `GUILD_ID`.

Inside, add the following two lines:

```text
BOT_TOKEN=YourDiscordBotTokenHere
GUILD_ID=YourDiscordTestServerIdHere
```
See [here](../creating-bot-account) for help with obtaining the bot token, and [here](../obtaining-discord-ids#guild-id) for help with obtaining the guild's ID.


##### 1.2 Setting up the script environment
The bootstrapping script is a Python program so you will need a compatible Python version and the necessary dependencies installed,
which are all detailed here:

1. Make sure you have [Python 3.10](https://www.python.org/downloads/) installed. It helps if it is your system's default Python version.
2. [Install Poetry](https://github.com/python-poetry/poetry#installation).
3. [Install the dependencies](../installing-project-dependencies).

#### 2. Running the script

Once the script setup phase is complete, all that is left is to run it.
To do this, you'll simply need to run the `configure` poetry task:

```shell
$ poetry run task configure
```

Once the script has finished running, you'll notice the creation of a new file called [`.env.server`](#envserver) at your project's root directory.
This file will contain the extracted IDs from your server which are necessary for your bot to run.

**Congratulations**, you have finished the configuration and can now [run your bot](#run-it).


#### Manual configuration

**Note**: Skip this part if you used the automatic configuration.

##### .env.server
Reading this means that you're ready for a bit of manual labour.
If for some reason you've missed the automatic server setup section, you can read about it [here](#automatic-configuration)

To configure the bot manually, you will **only** need to set the values for the channels, roles, categories, etc.
that are used by the component you are developing.

For example, if we're testing a feature that only needs the `announcements` channel:

`constants.py`

```py

class EnvConfig:
    # Defines from where & how Pydantic will be looking for env variables
    ...

class _Channels(EnvConfig):

    EnvConfig.Config.env_prefix = "channels_"

    announcements = 1079790565794779156
    changelog = 1077877318564991006

# Instantiate the class & load the configuration
Channels = _Channels()
```

`.env.server` file:

```text
# .env.server

channels_announcements=1077875228002234398
```

When you launch your bot, `pydantic` will load up the server constants from the `.env.server` file if they exist.

Each constants class will define its own prefix, which will make `pydantic` look for variables that will look like `{{env_prefix}}{{attribute_name}}` in the environment files

In our example, this will imply that pydantic will look for both `channels_announcements` and `channels_changelog` in the `.env.server` file.

As you can see here, only `channels_announcements` has been defined in the `.env.server` file since it's the only one needed, which will tell `pydantic`
to use the value **1077875228002234398** for the `announcements` attribute instead of the default **1079790565794779156**, and use the default value for the `changelog` attribute

```python
>>> Channels.announcements
1077875228002234398
>>> Channels.changelong
1077877318564991006
```

See [here](../obtaining-discord-ids) for help with obtaining Discord IDs.

If you wish to set all values in your `env.server` for your testing server, you need to set **all** the ones prefixed with:

* `guild_`
* `categories_`
* `channels_`
* `roles_`
* `webhooks_`
* `emojis_`

Additionally:

* At this stage, set `redis_use_fakeredis=true`. If you're looking for instructions for working with Redis, see [Working with Redis](#optional-working-with-redis).

We understand this is tedious which is why we **heavily recommend** using the [automatic configuration setup](#automatic-configuration)

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

##### .env
The second file you need to create is the one containing the environment variables, and needs to be named `.env`.
Inside, add the line `BOT_TOKEN=YourDiscordBotTokenHere`. See [here](../creating-bot-account) for help with obtaining the bot token.

---


### Run it!
#### With Docker
You are now almost ready to run the Python bot. The simplest way to do so is with Docker.

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

In your `.env.server` file:

* If you wish to work with snekbox, set the following:
    * `urls_snekbox_eval_api` to `"http://snekbox:8060/eval"`
    * `urls_snekbox_311_eval_api` to `"http://snekbox-311:8060/eval"`.



Assuming you have Docker installed **and running**, enter the cloned repo in the command line and type `docker-compose up`.

If working with snekbox you can run `docker-compose --profile 3.10 up` to also start up a 3.10 snekbox container, in addition to the default 3.11 container!

After pulling the images and building the containers, your bot will start. Enter your server and type `!help` (or whatever prefix you chose instead of `!`).

Your bot is now running, but this method makes debugging with an IDE a fairly involved process. For additional running methods, continue reading the following sections.

#### With the Bot Running Locally
The advantage of this method is that you can run the bot's code in your preferred editor, with debugger and all, while keeping all the setup of the bot's various dependencies inside Docker.

* Append the following line to your `.env` file: `API_KEYS_SITE_API=badbot13m0n8f570f942013fc818f234916ca531`.
* In your `.env.server` file, set `urls_site_api="http://localhost:8000/api"`. If you wish to keep using `http://web:8000/api`, then [COMPOSE_PROJECT_NAME](../docker/#compose-project-names) has to be set.
* To work with snekbox, set `urls_snekbox_eval_api="http://localhost:8060/eval"` and `urls_snekbox_311_eval_api="http://localhost:8065/eval"`


You will need to start the services separately, but if you got the previous section with Docker working, that's pretty simple:

* `docker-compose up web` to start the site container. This is required.
* `docker-compose up snekbox` to start the snekbox container. You only need this if you're planning on working on the snekbox cog.
* `docker-compose up snekbox-311` to start the snekbox 3.11 container. You only need this if you're planning on working on the snekbox cog.
* `docker-compose up redis` to start the Redis container. You only need this if you're not using fakeredis. For more info refer to [Working with Redis](#optional-working-with-redis).

You can start several services together: `docker-compose up web snekbox redis`.

##### Setting Up a Development Environment
The bot's code is Python code like any other. To run it locally, you will need the right version of Python with the necessary packages installed:

1. Make sure you have [Python 3.10](https://www.python.org/downloads/) installed. It helps if it is your system's default Python version.
2. [Install Poetry](https://github.com/python-poetry/poetry#installation).
3. [Install the dependencies](../installing-project-dependencies).

With at least the site running in Docker already (see the previous section on how to start services separately), you can now start the bot locally through the command line, or through your preferred IDE.
<div class="card">
    <button type="button" class="card-header collapsible">
        <span class="card-header-title subtitle is-6 my-2 ml-2">Ways to run code</span>
        <span class="card-header-icon">
            <i class="fas fa-fw fa-angle-down title is-5" aria-hidden="true"></i>
        </span>
    </button>
    <div class="collapsible-content collapsed">
        <div class="card-content">
            Notice that the bot is started as a module. There are several ways to do so:
            <ul>
                <li>Through the command line, inside the bot directory, with either <code>poetry run task start</code>, or directly <code>python -m bot</code>.</li>
                <li>If using PyCharm, enter <code>Edit Configurations</code> and set everything according to this image: <img src="/static/images/content/contributing/pycharm_run_module.png"></li>
                <li>If using Visual Studio Code, set the interpreter to the poetry environment you created. In <code>launch.json</code> create a new Python configuration, and set the name of the program to be run to <code>bot</code>. VSC will correctly run it as a module.</li>
            </ul>
        </div>
    </div>
</div>
<br>

#### With More Things Running Locally
You can run additional services on the host, but this guide won't go over how to install and start them in this way.
If possible, prefer to start the services through Docker to replicate the production environment as much as possible.

The site, however, is a mandatory service for the bot.
Refer to the [previous section](#with-the-bot-running-locally) and the [site contributing guide](../site) to learn how to start it on the host, in which case you will need to change `urls.site` in `.env.server` to wherever the site is being hosted.

---
### Development Tips
Now that you have everything setup, it is finally time to make changes to the bot!

#### Working with Git

Version control of our projects is done using Git and Github.
It can be intimidating at first, so feel free to ask for any help in the server.

[**Click here to see the basic Git workflow when contributing to one of our projects.**](../working-with-git/)

#### Running tests

[This section](https://github.com/python-discord/bot/blob/main/tests/README.md#tools) of the README in the `tests` repository will explain how to run tests.
The whole document explains how unittesting works, and how it fits in the context of our project.

Make sure to run tests *before* pushing code.

Even if you run the bot through Docker, you might want to [setup a development environment](#setting-up-a-development-environment) in order to run the tests locally.

#### Lint before you push
As mentioned in the [contributing guidelines](../contributing-guidelines), you should make sure your code passes linting for each commit you make.

For ease of development, you can install the pre-commit hook with `poetry run task precommit`, which will check your code every time you try to commit it.
For that purpose, even if you run the bot through Docker, you might want to [setup a development environment](#setting-up-a-development-environment), as otherwise the hook installation will fail.

#### Reloading parts of the bot
If you make changes to an extension, you might not need to restart the entire bot for the changes to take effect. The command `!ext reload <extension_name>` re-imports the files associated with the extension.
Invoke `!ext list` for a full list of the available extensions. In this bot in particular, cogs are defined inside extensions.

Note that if you changed code that is not associated with a particular extension, such as utilities, converters, and constants, you will need to restart the bot.

#### Adding new statistics

Details on how to add new statistics can be found on the [statistic infrastructure page](https://blog.pythondiscord.com/statistics-infrastructure).
We are always open to more statistics so add as many as you can!

---

### Optional: Working with the help forum

**Note**: This is only required when you're not configuring the bot [automatically](#automatic-configuration)

If you will be working on a feature that includes the python help forum, you will need to use `Forum Channels`.

Forum channels cannot be included in a template, which is why this needs to be done by hand for the time being.

To activate forum channels, your Discord server needs to have the community feature.
If that's not the case already, here are the steps required to do it:
1. Go to server settings
2. Scroll down to the `COMMUNITY` section and click on `Enable Community`
3. Click on `Get Started` and fill out the necessary info

Once the previous steps are done, all that is left is to:
1. Create a new channel
2. Choose the `Forum` type
3. [Copy its ID](../obtaining-discord-ids#channel-id)
4. Add the following line to the `.env.server` file: `channels_python_help={newly_created_forum_channel_id}`

---

### Optional: Working with Redis
In [Configure the Bot](#envserver) you were asked to set `redis_use_fakeredis=true`. If you do not need to work on features that rely on Redis, this is enough. Fakeredis will give the illusion that features relying on Redis are saving information properly, but restarting the bot or the specific cog will wipe that information.

If you are working on a feature that relies on Redis, you will need to enable Redis to make sure persistency is achieved for the feature across restarts. The first step towards that is going to `.env.server` and setting `redis.use_fakeredis` to `false`.

#### Starting Redis in Docker (Recommended)
If you're using the Docker image provided in the project's Docker Compose, open your `.env.server` file. If you're running the bot in Docker, set `redis_host=redis`, and if you're running it on the host set it to `localhost`. Set `redis_password=""`.

#### Starting Redis Using Other Methods
You can run your own instance of Redis, but in that case you will need to correctly set `redis_host` and `redis_port` in your `.env.server` file and the `REDIS_PASSWORD` in the `.env` file.
**Note**: The previously mentioned variables **SHOULD NOT** be overriden or changed in `constants.py`

---

### Optional: Working with Metricity
[Metricity](https://github.com/python-discord/metricity) is our home-grown bot for collecting metrics on activity within the server, such as what users are  present, and IDs of the messages they've sent.
Certain features in the Python bot rely on querying the Metricity database for information such as the number of messages a user has sent, most notably the voice verification system.

If you wish to work on a feature that relies on Metricity, for your convenience we've made the process of using it relatively painless with Docker: Enter the `.env` file you've written for the Python bot, and append the line `USE_METRICITY=true`.
Note that if you don't need Metricity, there's no reason to have it enabled as it is just unnecessary overhead.

To make the Metricity bot work with your test server, you will need to override its configurations similarly to the Python bot.
You can see the various configurations in [the Metricity repo](https://github.com/python-discord/metricity), but the bare minimum is the guild ID setting.
In your local version of the Python bot repo, create a file called `metricity-config.toml` and insert the following lines:
```yaml
[bot]
guild_id = replace_with_your_guild_id
```
To properly replicate production behavior, set the `staff_role_id`, `staff_categories`, and `ignore_categories` fields as well.

Now, `docker-compose up` will also start Metricity.

If you want to run the bot locally, you can run `docker-compose up metricity` instead.

---

### Optional: Working with bot moderation logs
To be able to view moderation-related logs published by the bot to site, you will need to set `urls_site_logs_view=http://localhost:8000/staff/bot/logs` in your `.env.server`.
This will work in both Docker and locally.

---

### Optional: Changing your command prefix
If you would like a prefix other than the default `!`, set `BOT_PREFIX={{your_prefix}}` in `.env.server`.

---

### Issues?
If you have any issues with setting up the bot, come discuss it with us on the [#dev-contrib](https://discord.gg/2h3qBv8Xaa) channel on our server.

If you find any bugs in the bot or would like to request a feature, feel free to [open an issue](https://github.com/python-discord/bot/issues/new/choose) on the repository.

---

### Appendix: Full ENV File Options
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
| `REDIS_PASSWORD`     | When not using FakeRedis                          | The password to connect to the Redis database (see [Optional: Working with Redis](#optional-working-with-redis)).                                                                                                                                   |
| `USE_METRICITY`      | When using Metricity                              | `true` or `false`, depending on whether to enable metrics collection using Metricity (see [Optional: Working with Metricity](#optional-working-with-metricity)). `false` by default.                                                                |
| `API_KEYS_GITHUB`    | When you wish to interact with GitHub             | The API key to interact with GitHub, for example to download files for the branding manager.                                                                                                                                                        |
| `METABASE_USERNAME`  | When you wish to interact with Metabase           | The username for a Metabase admin account.                                                                                                                                                                                                          |
| `METABASE_PASSWORD`  | When you wish to interact with Metabase           | The password for a Metabase admin account.                                                                                                                                                                                                          |

---

# Next steps
Now that you have everything setup, it is finally time to make changes to the bot! If you have not yet read the [contributing guidelines](../contributing-guidelines.md), now is a good time. Contributions that do not adhere to the guidelines may be rejected.

If you're not sure where to go from here, our [detailed walkthrough](../#2-set-up-the-project) is for you.

Have fun!
