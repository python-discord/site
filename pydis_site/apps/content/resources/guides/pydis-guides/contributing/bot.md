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
You now have both the bot's code and a server to run it on. It's time you to connect the two by changing the bot's configurations.
This can be done either automatically or manually, and we'll be detailing the steps for both.

#### Automatic configuration
To make setup much easier, there is a file called `bootstrap_config.py` that represents a script to bootstrap the configuration for you and help you get started immediately
without having to spend much time copying ids from your newly created server into your configuration file.

**Note**: This phase can be skipped and done manually, but would require extra manual work.

##### 1. Script setup
##### 1.1. Environment variables
You will need to create a file called `.env` which will contain two required values for the script to work: `BOT_TOKEN` and `GUILD_ID`
Inside, add the following two lines:

```text
BOT_TOKEN=YourDiscordBotTokenHere
GUILD_ID=YourDiscordTestServerIdHere
```
See [here](../creating-bot-account) for help with obtaining the bot token and [here](../obtaining-discord-ids#guild-id) for help with obtaining the guild's id

**Note**: The `.env` file will be ignored by commits.
##### 1.2 Setting up the script environment
The bootstrapping script is Python code like any other. To run it locally, you will need the right version of Python with the necessary packages installed:
1. Make sure you follow steps `1` and `2` [here](#setting-up-a-development-environment)
2. [Install the `config-bootstrap` dependency group](../installing-project-dependencies#installing-specific-dependency-groups).

#### 2. Running the script

Once the script setup phase is complete, all that is left is to run it.
To do this, you'll simply need to run the `configure` poetry task like this

```shell
$ poetry run task configure
```

or, without poetry and from the root directory

```shell
python3 -m bootstrap_config
```

Once the script has finished running, you'll notice the creation of a new file called [`.env.server`](#envserver) at your project's root directory.
This file will contain the extracted ids from your newly created server which are necessary for your bot to run.
Congratulations, you have finished the configuration & can now start [running your bot](#run-it-)

#### Manual configuration
##### .env.server
All server configuration values are saved in a file called `.env.server`, which needs to be at the root directory of the cloned code.
This file contains the various configurations we use to make the bot run on the Python Discord server, such as channel and role IDs, and the emojis it works with.
It also contains configurations such as how long it takes for a help channel to time out, and how many messages a user needs to voice-verify.

If you decided to use the bootstrapping script, you'll find that this file has already been created (which we recommend),
otherwise you'll need to create it manually.

To run the bot in your test server, you will **only** need to add the **necessary** configuration values for the channels/roles/categories, etc.
that you'll be using for testing

Let's take an example where we suppose we'll only be testing a feature that needs the `announcements` channel.

`constants.py`

```py

from pydantic import Field

class EnvConfig:
    # Defines from where & how Pydantic will be looking for env variables
    ...

class _Channels(EnvConfig):

    EnvConfig.Config.env_prefix = "channels."

    announcements: int = Field(default=123)
    changelog: int = Field(default=456)

# Instantiate the class & load the configuration
Channels = _Channels()
```

`.env.server` file

```text
channels.announcements=789
```

When you launch your bot, `pydantic` will load up the server constants from the `.env.server` file if they exist.

Each constants class will define its own prefix, which will make `pydantic` look for variables that will look like `{{env_prefix}}{{attribute_name}}` in the environment files

In our example, this will imply that pydantic will look for both `channels.announcements` and `channels.changelog` in the `.env.server` file.

As you can see here, only `channels.announcements` has been defined in the `.env.server` file since it's the only one needed, which will tell `pydantic`
to use the value **789** for the `announcements` attribute instead of the default **456**, and use the default value for the `changelog` attribute

```python
>>> Channels.announcements
789
>>> Channels.changelong
456
```

See [here](../obtaining-discord-ids) for help with obtaining Discord IDs.

<div class="card">
    <button type="button" class="card-header collapsible">
        <span class="card-header-title subtitle is-6 my-2 ml-2">Full .env.server appendix</span>
        <span class="card-header-icon">
            <i class="fas fa-fw fa-angle-down title is-5" aria-hidden="true"></i>
        </span>
    </button>
    <div class="collapsible-content collapsed">
        <div class="card-content">
              <p>If you used the provided server template, and you're not sure which channels belong where in the config file, you can use the config below. Pay attention to the comments with several <code>#</code> symbols, and replace the <code>�</code> characters with the right IDs.</p>
              <pre>

# Channels configuration
channels.announcements=�
channels.changelog=�
channels.mailing_lists=�
channels.python_events=�
channels.python_news=�
channels.reddit=�

channels.dev_contrib=�
channels.dev_core=�
channels.dev_log=�

channels.meta=�
channels.python_general=�

channels.help_system_forum=�

channels.attachment_log=�
channels.filter_log=�
channels.message_log=�
channels.mod_log=�
channels.nomination_archive=�
channels.user_log=�
channels.voice_log=�

channels.off_topic_0=�
channels.off_topic_1=�
channels.off_topic_2=�

channels.bot_commands=�
channels.discord_bots=�
channels.esoteric=�
channels.voice_gate=�
channels.code_jam_planning=�

### Staff
channels.admins=�
channels.admin_spam=�
channels.defcon=�
channels.helpers=�
channels.incidents=�
channels.incidents_archive=�
channels.mod_alerts=�
channels.mod_meta=�
channels.mods=�
channels.nominations=�
channels.nomination_voting=�
channels.organisation=�

### Staff announcement channels
channels.admin_announcements=�
channels.mod_announcements=�
channels.staff_announcements=�
channels.staff_info=�
channels.staff_lounge=�

### Voice Channels
channels.admins_voice=�
channels.code_help_voice_0=�
channels.code_help_voice_1=�
channels.general_voice_0=�
channels.general_voice_1=�
channels.staff_voice=�

channels.black_formatter=�

### Voice Chat
channels.code_help_chat_0=�
channels.code_help_chat_1=�
channels.staff_voice_chat=�
channels.voice_chat_0=�
channels.voice_chat_1=�

channels.big_brother_logs=�
channels.duck_pond=�
channels.roles=�

# Roles configuration

roles.advent_of_code=�
roles.announcements=�
roles.lovefest=�
roles.pyweek_announcements=�
roles.revival_of_code=�
roles.legacy_help_channels_access=�

roles.contributors=�
roles.help_cooldown=�
roles.muted=�
roles.partners=�
roles.python_community=�
roles.sprinters=�
roles.voice_verified=�

### Streaming
roles.video=�

### Staff
roles.admins=�
roles.core_developers=�
roles.code_jam_event_team=�
roles.devops=�
roles.domain_leads=�
roles.events_lead=�
roles.helpers=�
roles.moderators=�
roles.mod_team=�
roles.owners=�
roles.project_leads=�

### Code Jam
roles.jammers=�

### Patreon
roles.patreon_tier_1=�
roles.patreon_tier_2=�
roles.patreon_tier_3=�



# Categories configuration

categories.logs=�
categories.moderators=�
categories.modmail=�
categories.appeals=�
categories.appeals2=�
categories.voice=�

### 2021 Summer Code Jam
categories.summer_code_jam=�


# Guild configuration
guild.id=�
guild.invite="https://discord.gg/python"


# Webhooks configuration

webhooks.big_brother.id=�
webhooks.dev_log.id=�
webhooks.duck_pond.id=�
webhooks.incidents.id=�
webhooks.incidents_archive.id=�
webhooks.python_news.id=�

# Big brother configuration
big_brother.header_message_limit=15
big_brother.log_delay=15

# Code Block configuration

code_block.cooldown_seconds=300
code_block.minimum_lines=4


# Colours configuration

colours.blue=0x3775a8
colours.bright_green=0x01d277
colours.orange=0xe67e22
colours.pink=0xcf84e0
colours.purple=0xb734eb
colours.soft_green=0x68c290
colours.soft_orange=0xf9cb54
colours.soft_red=0xcd6d6d
colours.white=0xfffffe
colours.yellow=0xffd241

# Free configuration
free.activity_timeout=600
free.cooldown_per=60.0
free.cooldown_rate=1

# Antispam configuration
antispam.rules.attachments.interval=10
antispam.rules.attachments.max=10

antispam.rules.burst.interval=10
antispam.rules.burst.max=7

antispam.rules.chars.interval=5
antispam.rules.chars.max=200

antispam.rules.discord_emojis.interval=10
antispam.rules.discord_emojis.max=20

antispam.rules.duplicates.interval=10
antispam.rules.duplicates.max=3

antispam.rules.links.interval=10
antispam.rules.links.max=10

antispam.rules.mentions.interval=10
antispam.rules.mentions.max=5

antispam.rules.newlines.interval=10
antispam.rules.newlines.max=100
antispam.rules.newlines.max_consecutive=10

antispam.rules.role_mentions.interval=10
antispam.rules.role_mentions.max=3


antispam.cache_size=100
antispam.clean_offending=true
antispam.ping_everyone=true
antispam.punishment.remove_after=600


# Help channels configuration
help_channels.enable=true
help_channels.idle_minutes=30
help_channels.deleted_idle_minutes=5

# Redirect output configuration
redirect_output.delete_delay=15
redirect_output.delete_invocation=true

# Duck pond configuration
duckpond.threshold=7

# Python news configuration
python_news.mail_lists=

# Voice gate configuration
voice_gate.bot_message_delete_delay=10
voice_gate.minimum_activity_blocks=3
voice_gate.minimum_days_member=3
voice_gate.minimum_messages=50
voice_gate.voice_ping_delete_delay=60

# Branding configuration
branding.cycle_frequency=3

# Video permisions configuration
video_permission.default_permission_duration=5

# Redis configuration
redis.host="redis.default.svc.cluster.local"
redis.port=6379
redis.use_fakeredis=false  # If this is true, Bot will use fakeredis.aioredis

# Cleaning configuration
clean.message_limit=10000

# Stats configuration
stats.presence_update_timeout=30
stats.statsd_host="graphite.default.svc.cluster.local"

# Cooldowns configuration
cooldowns.tags=60

# Metabase configuration
metabase.base_url="http://metabase.default.svc.cluster.local"
metabase.public_url="https://metabase.pythondiscord.com"
metabase.max_session_age=20_160

# URLs configuration

urls.snekbox_eval_api="http://snekbox.default.svc.cluster.local/eval"
urls.snekbox_311_eval_api="http://snekbox-311.default.svc.cluster.local/eval"

# Discord API
urls.discord_api="https://discordapp.com/api/v7/"

# Misc endpoints
urls.bot_avatar="https://raw.githubusercontent.com/python-discord/branding/main/logos/logo_circle/logo_circle.png"
urls.github_bot_repo=https://github.com/python-discord/bot

# Site
urls.site="pythondiscord.com"
urls.site_schema="https://"
urls.site_api="site.default.svc.cluster.local/api"
urls.site_api_schema="http://"

urls.connect_max_retries=3
urls.connect_cooldown=5


# Emojis configuration
emojis.badge_bug_hunter="<:bug_hunter_lvl1:743882896372269137>"
emojis.badge_bug_hunter_level_2="<:bug_hunter_lvl2:743882896611344505>"
emojis.badge_early_supporter="<:early_supporter:743882896909140058>"
emojis.badge_hypesquad="<:hypesquad_events:743882896892362873>"
emojis.badge_hypesquad_balance="<:hypesquad_balance:743882896460480625>"
emojis.badge_hypesquad_bravery="<:hypesquad_bravery:743882896745693335>"
emojis.badge_hypesquad_brilliance="<:hypesquad_brilliance:743882896938631248>"
emojis.badge_partner="<:partner:748666453242413136>"
emojis.badge_staff="<:discord_staff:743882896498098226>"
emojis.badge_verified_bot_developer="<:verified_bot_dev:743882897299210310>"
emojis.verified_bot="<:verified_bot:811645219220750347>"
emojis.bot="<:bot:812712599464443914>"

emojis.defcon_shutdown="<:defcondisabled:470326273952972810>"  # noqa: E704
emojis.defcon_unshutdown="<:defconenabled:470326274213150730>"  # noqa: E704
emojis.defcon_update="<:defconsettingsupdated:470326274082996224>"  # noqa: E704

emojis.failmail="<:failmail:633660039931887616>"

emojis.incident_actioned="<:incident_actioned:714221559279255583>"
emojis.incident_investigating="<:incident_investigating:714224190928191551>"
emojis.incident_unactioned="<:incident_unactioned:714223099645526026>"

emojis.status_dnd="<:status_dnd:470326272082313216>"
emojis.status_idle="<:status_idle:470326266625785866>"
emojis.status_offline="<:status_offline:470326266537705472>"
emojis.status_online="<:status_online:470326272351010816>"

emojis.ducky_dave="<:ducky_dave:742058418692423772>"

emojis.trashcan="<:trashcan:637136429717389331>"

emojis.bullet="\u2022"
emojis.check_mark="\u2705"
emojis.cross_mark="\u274C"
emojis.new="\U0001F195"
emojis.pencil="\u270F"

emojis.ok_hand=":ok_hand:"

# Icons configuration

icons.crown_blurple="https://cdn.discordapp.com/emojis/469964153289965568.png"
icons.crown_green="https://cdn.discordapp.com/emojis/469964154719961088.png"
icons.crown_red="https://cdn.discordapp.com/emojis/469964154879344640.png"

icons.defcon_denied="https://cdn.discordapp.com/emojis/472475292078964738.png"
icons.defcon_shutdown="https://cdn.discordapp.com/emojis/470326273952972810.png"
icons.defcon_unshutdown="https://cdn.discordapp.com/emojis/470326274213150730.png"
icons.defcon_update="https://cdn.discordapp.com/emojis/472472638342561793.png"

icons.filtering="https://cdn.discordapp.com/emojis/472472638594482195.png"

icons.green_checkmark="https://raw.githubusercontent.com/python-discord/branding/main/icons/checkmark/green-checkmark-dist.png"
icons.green_questionmark="https://raw.githubusercontent.com/python-discord/branding/main/icons/checkmark/green-question-mark-dist.png"

icons.guild_update="https://cdn.discordapp.com/emojis/469954765141442561.png"

icons.hash_blurple="https://cdn.discordapp.com/emojis/469950142942806017.png"
icons.hash_green="https://cdn.discordapp.com/emojis/469950144918585344.png"
icons.hash_red="https://cdn.discordapp.com/emojis/469950145413251072.png"

icons.message_bulk_delete="https://cdn.discordapp.com/emojis/469952898994929668.png"
icons.message_delete="https://cdn.discordapp.com/emojis/472472641320648704.png"
icons.message_edit="https://cdn.discordapp.com/emojis/472472638976163870.png"

icons.pencil="https://cdn.discordapp.com/emojis/470326272401211415.png"

icons.questionmark="https://cdn.discordapp.com/emojis/512367613339369475.png"

icons.remind_blurple="https://cdn.discordapp.com/emojis/477907609215827968.png"
icons.remind_green="https://cdn.discordapp.com/emojis/477907607785570310.png"
icons.remind_red="https://cdn.discordapp.com/emojis/477907608057937930.png"

icons.sign_in="https://cdn.discordapp.com/emojis/469952898181234698.png"
icons.sign_out="https://cdn.discordapp.com/emojis/469952898089091082.png"

icons.superstarify="https://cdn.discordapp.com/emojis/636288153044516874.png"
icons.unsuperstarify="https://cdn.discordapp.com/emojis/636288201258172446.png"

icons.token_removed="https://cdn.discordapp.com/emojis/470326273298792469.png"

icons.user_ban="https://cdn.discordapp.com/emojis/469952898026045441.png"
icons.user_mute="https://cdn.discordapp.com/emojis/472472640100106250.png"
icons.user_unban="https://cdn.discordapp.com/emojis/469952898692808704.png"
icons.user_unmute="https://cdn.discordapp.com/emojis/472472639206719508.png"
icons.user_update="https://cdn.discordapp.com/emojis/469952898684551168.png"
icons.user_verified="https://cdn.discordapp.com/emojis/470326274519334936.png"
icons.user_warn="https://cdn.discordapp.com/emojis/470326274238447633.png"

icons.voice_state_blue="https://cdn.discordapp.com/emojis/656899769662439456.png"
icons.voice_state_green="https://cdn.discordapp.com/emojis/656899770094452754.png"
icons.voice_state_red="https://cdn.discordapp.com/emojis/656899769905709076.png"

# Filters configuration
filters.filter_domains=true
filters.filter_everyone_ping=true
filters.filter_invites=true
filters.filter_zalgo=false
filters.watch_regex=true
filters.watch_rich_embeds=true

### Notifications are not expected for "watchlist" type filters

filters.notify_user_domains=false
filters.notify_user_everyone_ping=true
filters.notify_user_invites=true
filters.notify_user_zalgo=false

filters.offensive_msg_delete_days=7
filters.ping_everyone=true

</pre>
</div></div></div>
<br>


If you don't wish to use the provided `env.server` above, the main values that need overriding are **all** the ones prefixed with:

* `guild.`
* `categories.`
* `channels.`
* `roles.`
* `webhooks.`
* `emojis.`

Additionally:

* At this stage, set `redis.use_fakeredis` to `true`. If you're looking for instructions for working with Redis, see [Working with Redis](#optional-working-with-redis).
* Set `urls.site_schema` and `urls.site_api_schema` to `"http://"`.

We understand this is tedious which is why we **recommend** using the [automatic configuration setup](#automatic-configuration)

<div class="card">
    <button type="button" class="card-header collapsible">
        <span class="card-header-title subtitle is-6 my-2 ml-2">Why do you need a separate config file?</span>
        <span class="card-header-icon">
            <i class="fas fa-fw fa-angle-down title is-5" aria-hidden="true"></i>
        </span>
    </button>
    <div class="collapsible-content collapsed">
        <div class="card-content">
            While it's technically possible to edit the values in `constants.py` to match your server, it is heavily discouraged.
            This file's purpose is to provide the configurations the Python bot needs to run in the Python server in production, and should remain as such.
            In contrast, the <code>.env.server</code> file can remain in your local copy of the code, and will be ignored by commits via the project's <code>.gitignore</code>.
        </div>
    </div>
</div>
<br>

##### .env
The second file you need to create is the one containing the environment variables, and needs to be named `.env`.
Inside, add the line `BOT_TOKEN=YourDiscordBotTokenHere`. See [here](../creating-bot-account) for help with obtaining the bot token.

**Note**: The `.env` file will be ignored by commits.

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

* Set `urls.site` to `"web:8000"`.
* If you wish to work with snekbox set the following:
    * `urls.snekbox_eval_api` to `"http://snekbox:8060/eval"`
    * `urls.snekbox_311_eval_api` to `"http://snekbox-311:8060/eval"`.

Assuming you have Docker installed **and running**, enter the cloned repo in the command line and type `docker-compose up`.

If working with snekbox you can run `docker-compose --profile 3.10 up` to also start up a 3.10 snekbox container, in addition to the default 3.11 container!

After pulling the images and building the containers, your bot will start. Enter your server and type `!help` (or whatever prefix you chose instead of `!`).

Your bot is now running, but this method makes debugging with an IDE a fairly involved process. For additional running methods, continue reading the following sections.

#### With the Bot Running Locally
The advantage of this method is that you can run the bot's code in your preferred editor, with debugger and all, while keeping all the setup of the bot's various dependencies inside Docker.

* Append the following line to your `.env` file: `BOT_API_KEY=badbot13m0n8f570f942013fc818f234916ca531`.
* In your `.env.server` file, set `urls.site` to `"localhost:8000"`. If you wish to keep using `web:8000`, then [COMPOSE_PROJECT_NAME](../docker/#compose-project-names) has to be set.
* To work with snekbox, set `urls.snekbox_eval_api` to `"http://localhost:8060/eval"` and `urls.snekbox_311_eval_api` to `"http://localhost:8065/eval"`

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

### Optional: Working with Redis
In [Configure the Bot](#envserver) you were asked to set `redis.use_fakeredis` to `true`. If you do not need to work on features that rely on Redis, this is enough. Fakeredis will give the illusion that features relying on Redis are saving information properly, but restarting the bot or the specific cog will wipe that information.

If you are working on a feature that relies on Redis, you will need to enable Redis to make sure persistency is achieved for the feature across restarts. The first step towards that is going to `.env.server` and setting `redis.use_fakeredis` to `false`.

#### Starting Redis in Docker (Recommended)
If you're using the Docker image provided in the project's Docker Compose, open your `.env.server` file. If you're running the bot in Docker, set `redis.host` to `redis`, and if you're running it on the host set it to `localhost`. Set `bot.redis.password` to `""`.

#### Starting Redis Using Other Methods
You can run your own instance of Redis, but in that case you will need to correctly set `redis.host` and `redis.port`, and the `redis.password` value in `constants.py` should not be overridden. Then, enter the `.env` file, and set `REDIS_PASSWORD` to whatever password you set.

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

### Issues?
If you have any issues with setting up the bot, come discuss it with us on the [#dev-contrib](https://discord.gg/2h3qBv8Xaa) channel on our server.

If you find any bugs in the bot or would like to request a feature, feel free to open an issue on the repository.

---

### Appendix: Full ENV File Options
The following is a list of all available environment variables used by the bot:

| Variable             | Required                                        | Description                                                                                                                                                                                                                                         |
|----------------------|-------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `BOT_TOKEN`          | Always                                          | Your Discord bot account's token (see [Set Up a Bot Account](#set-up-a-bot-account)).                                                                                                                                                               |
| `GUILD_ID`           | When using the bootstrapping script             | Your Discord test server's id (see [Set Up a Test Server](#set-up-a-test-server)).                                                                                                                                                                  |
| `BOT_API_KEY`        | When running bot without Docker                 | Used to authenticate with the site's API. When using Docker to run the bot, this is automatically set. By default, the site will always have the API key shown in the example below.                                                                |
| `BOT_SENTRY_DSN`     | When connecting the bot to sentry               | The DSN of the sentry monitor.                                                                                                                                                                                                                      |
| `BOT_TRACE_LOGGERS ` | When you wish to see specific or all trace logs | Comma separated list that specifies which loggers emit trace logs through the listed names. If the ! prefix is used, all of the loggers except the listed ones are set to the trace level. If * is used, the root logger is set to the trace level. |
| `BOT_DEBUG`          | In production                                   | `true` or `false`, depending on whether to enable debug mode, affecting the behavior of certain features. `true` by default.                                                                                                                        |
| `REDIS_PASSWORD`     | When not using FakeRedis                        | The password to connect to the Redis database (see [Optional: Working with Redis](#optional-working-with-redis)).                                                                                                                                   |
| `USE_METRICITY`      | When using Metricity                            | `true` or `false`, depending on whether to enable metrics collection using Metricity (see [Optional: Working with Metricity](#optional-working-with-metricity)). `false` by default.                                                                |
| `GITHUB_API_KEY`     | When you wish to interact with GitHub           | The API key to interact with GitHub, for example to download files for the branding manager.                                                                                                                                                        |
| `METABASE_USERNAME`  | When you wish to interact with Metabase         | The username for a Metabase admin account.                                                                                                                                                                                                          |
| `METABASE_PASSWORD`  | When you wish to interact with Metabase         | The password for a Metabase admin account.                                                                                                                                                                                                          |

---

# Next steps
Now that you have everything setup, it is finally time to make changes to the bot! If you have not yet read the [contributing guidelines](../contributing-guidelines.md), now is a good time. Contributions that do not adhere to the guidelines may be rejected.

If you're not sure where to go from here, our [detailed walkthrough](../#2-set-up-the-project) is for you.

Have fun!
