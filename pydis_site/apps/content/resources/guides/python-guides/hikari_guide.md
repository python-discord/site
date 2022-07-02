---
title: Getting Started with Hikari
description: A guide for Discord bot development using hikari library.
toc: 2
---

## What is Hikari?

Hikari is a statically typed Python3 framework for working with the Discord REST API and Gateway.
The library focuses on being extendable and reusable, rather than an obstacle for future development.

Currently supported python versions: 3.8, 3.9, 3.10 <br>
Github Repository: [https://github.com/hikari-py/hikari](https://github.com/hikari-py/hikari) <br>
Documentation: [https://www.hikari-py.dev/hikari/index.html](https://www.hikari-py.dev/hikari/index.html) <br>
Support Server: [https://discord.com/invite/Jx4cNGG](https://discord.com/invite/Jx4cNGG) <br>

### Prequesties

- Python 3.8+
- Basic knowledge of python, which includes but is not limited to the points listed below.
  - Python data types
  - Object Oriented Programming, difference between class and class instances, etc.
  - asyncio and async/await syntax
  - Loops and iterators
  - `in`, `and`, `or`, `continue`, `break`, `return` statements
  - Flow control ( if/else/elif , match/case )
- A bot application

<details><summary><b>Creating a bot application and getting the token.</b></summary><br>
Go to the <a href="https://discord.com/developers/applications">Discord Developer Portal</a> and click on "New Application" to create a new app. <br><br>
<img src="https://raw.githubusercontent.com/sarthhh/hikari_guide/main/assets/portal1.png" alt="create application"> <br><br>
Go to the "Bot" menu and click on "Add bot" <br><br>
<img src="https://raw.githubusercontent.com/sarthhh/hikari_guide/main/assets/portal2.png" alt="create bot"><br><br>
You can then click on "Reset Token" to create a new bot token and copy it.<br><br>
<img src="https://raw.githubusercontent.com/sarthhh/hikari_guide/main/assets/portal3.png" alt="regen token">
</details>

---

### What is a bot token?

A bot token is a key that is used for authorization purposes by the discord API.
It is utilized by the library for connecting your bot with the API and handling requests.

### Installation

Linux/macOS: `python -m pip install -U hikari`

Windows: `py -3 pip install -U hikari`

### Basic Example

```py
import hikari  # importing the hikari library.

intents = hikari.Intents(
    hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT
)  # defining the intents to be used for the bot. It's set to `hikari.Intents.ALL_UNPRIVILEGED` by default.
bot = hikari.GatewayBot("bot token here", intents=intents,)  # creating a GatewayBot class instance which will be used to recieve events from the discord gateway.

@bot.listen()
async def message_created(event: hikari.MessageCreateEvent) -> None:
    """
    A simple MessageCreateEvent which sends Pong as a response for !ping.
    """

    if event.message.content == "!ping":
        await event.message.respond("Pong")


bot.run()  # calling the run function to run the bot.
```

<br>

## Events in Hikari

Payloads received from the discord gateway are converted to Event dataclasses and provided to the event listeners.

All the events are derived from the [`hikari.Event`](https://www.hikari-py.dev/hikari/events/base_events.html#hikari.events.base_events.Event) class.

### Creating Event listeners

`hikari.Gateway` class has a `listen` decorator that can be used to declare an asynchronous function as an event listener.

**Declaring an event listener**

```py
import hikari

bot = hikari.GatewayBot(
    "token",
    intents=hikari.Intents(
        hikari.Intents.ALL_UNPRIVILAGED | hikari.Intents.GUILD_MEMBERS
    ),
)

# you can either enter the event class in the .listen() decorator.
@bot.listen(hikari.MemberCreateEvent)
# or annotate the first-and-only argument of the function with the event class
async def member_joined(event: hikari.MemberCreateEvent) -> None:
    print(f"{event.member} joined a guild with ID: {event.guild_id}")

bot.run()
```

**Explanation**

- The `@bot.listen()` decorator is used to create an event listener (read the comments.)
- The event dataclass is passed as the first and only argument in that listener's function and can be used to access various methods and attributes related to the event.

You can find all the event classes listed [here](https://www.hikari-py.dev/hikari/events).

---

### Adding listeners without the .listen() decorator

There can be cases where you can't use the `bot.listen()` decorator, for example:

- while importing the listener function from another file.
- if you are subclassing `GatewayBot` and want to use a classmethod as a listener.

```py
import hikari

bot = hikari.GatewayBot("token",)

# the function on which @listen() decorator couldn't be used.
async def bot_started(event: hikari.StartedEvent) -> None:
    print("Bot is running!")


bot.event_manager.subscribe(hikari.StartedEvent, bot_started)

bot.run()
```

**Explanation**

- `bot.event_manager.subscribe()` calls the same method as the @listen decorator above used to add a listener to the bot.
- This method takes the event class as the first argument and the event function as the second one.

---

## Intents

Intents are Discord API feature that tells the gateway about which events you want your bot's WebSocket to receive.

By default, they are set to `98045` in hikari.GatewayBot which includes all intents except privileged intents.

### Enabling intents in code

For telling your GatewayBot what intents to request from discord, you need to pass a `hikari.Intents` object as the `intents` kwarg inside your GatewayBot object.

You can read about the functionality of all intents described here: [https://www.hikari-py.dev/hikari/index.html](https://www.hikari-py.dev/hikari/index.html)

**Creating Intents**

A `hikari.Intents` class can be initialized using intent enums mentioned with pipes ( `|` ) to declare the intents.

```py
import hikari

intents = hikari.Intents(
    hikari.Intents.ALL_GUILDS  # enables all guild related intents
    | hikari.Intents.DM_MESSAGES  # enables dm message intents
    | hikari.Intents.MESSAGE_CONTENT  # allows you to get message content from a message object, else it's None for servers
)
```

**Passing Intents to GatewayBot**

```py
bot = hikari.GatewayBot("token", intents=intents)
```

### Privileged Intents

Some intents need to be explicitly enabled from the Discord Developer portal to use them, which include:

- Member Intents
- Presence Intents
- Message Content Intents (applicable after 31 august)

These intents can be used freely for non-verified bots which need no data-whitelisting.
While verification, the application owner needs to request for these separately.
Read more about privileged intents [here](https://support.discord.com/hc/en-us/articles/360040720412)

<details><summary><b> Enabling Privileged Intents</b></summary>

<p>Go to <a href="https://discord.com/developers/applications">Discord Developer Portal</a> and select the bot application you want to enable the intents for.</p>
<p>Select the &quot;Bot&quot; menu in the sidebar.</p>
<p><img src="https://raw.githubusercontent.com/sarthhh/hikari_guide/main/assets/intents.png" alt="selecting menu"></p>
<p>Enable the intents you need.</p>
<p><img src="https://raw.githubusercontent.com/sarthhh/hikari_guide/main/assets/intents2.png" alt="toggle intents"></p>
<p>Save changes.</p>
<p><img src="https://raw.githubusercontent.com/sarthhh/hikari_guide/main/assets/intents3.png" alt="saving changes"></p>

</details>

<details><summary><b>Intents Table</b></summary>

<table>
<thead>
<tr>
<th>Intents</th>
<th>Value</th>
<th>Gateway Events</th>
</tr>
</thead>
<tbody>
<tr>
<td>DM_MESSAGES</td>
<td>4096</td>
<td>MESSAGE_CREATE<br>MESSAGE_UPDATE<br>MESSAGE_DELETE (DMs only.)</td>
</tr>
<tr>
<td>DM_MESSAGE_REACTIONS</td>
<td>8192</td>
<td>MESSAGE_REACTION_ADD<br>MESSAGE_REACTION_REMOVE<br>MESSAGE_REACTION_REMOVE_ALL<br>MESSAGE_REACTION_REMOVE_EMOJI (DMs only.)</td>
</tr>
<tr>
<td>DM_MESSAGE_TYPING</td>
<td>16384</td>
<td>TYPING_START (DMs only.)</td>
</tr>
<tr>
<td>GUILDS</td>
<td>1</td>
<td>GUILD_CREATE<br>GUILD_UPDATE<br>GUILD_DELETE<br>GUILD_ROLE_CREATE<br>GUILD_ROLE_UPDATE<br>GUILD_ROLE_DELETE<br>CHANNEL_CREATE<br>CHANNEL_UPDATE<br>CHANNEL_DELETE<br>CHANNEL_PINS_UPDATE</td>
</tr>
<tr>
<td>GUILD_BANS</td>
<td>4</td>
<td>GUILD_BAN_ADD<br>GUILD_BAN_REMOVE</td>
</tr>
<tr>
<td>GUILD_EMOJIS</td>
<td>8</td>
<td>GUILD_EMOJIS_UPDATE</td>
</tr>
<tr>
<td>GUILD_INTEGRATIONS</td>
<td>16</td>
<td>INTEGRATION_CREATE<br>INTEGRATION_DELETE<br>INTEGRATION_UPDATE</td>
</tr>
<tr>
<td>GUILD_INVITES</td>
<td>64</td>
<td>INVITE_CREATE<br>INVITE_DELETE</td>
</tr>
<tr>
<td>GUILD_MEMBERS*</td>
<td>2</td>
<td>GUILD_MEMBER_ADD<br>GUILD_MEMBER_UPDATE<br>GUILD_MEMBER_REMOVE</td>
</tr>
<tr>
<td>GUILD_MESSAGES</td>
<td>512</td>
<td>MESSAGE_CREATE (in guilds only)<br>MESSAGE_UPDATE (in guilds only)<br>MESSAGE_DELETE (in guilds only)<br>MESSAGE_BULK_DELETE (in guilds only)<br></td>
</tr>
<tr>
<td>GUILD_MESSAGE_REACTIONS</td>
<td>1024</td>
<td>MESSAGE_REACTION_ADD (in guilds only)<br>MESSAGE_REACTION_REMOVE (in guilds only)<br>MESSAGE_REACTION_REMOVE_ALL (in guilds only)<br>MESSAGE_REACTION_REMOVE_EMOJI (in guilds only)<br></td>
</tr>
<tr>
<td>GUILD_MESSAGE_TYPING</td>
<td>2048</td>
<td>TYPING_START (in guilds only)</td>
</tr>
<tr>
<td>GUILD_PRESENCES*</td>
<td>256</td>
<td>PRESENCE_UPDATE</td>
</tr>
<tr>
<td>GUILD_SCHEDULED_EVENTS</td>
<td>65536</td>
<td>GUILD_SCHEDULED_EVENT_CREATE<br>GUILD_SCHEDULED_EVENT_UPDATE<br>GUILD_SCHEDULED_EVENT_DELETE<br>GUILD_SCHEDULED_EVENT_USER_ADD<br>GUILD_SCHEDULED_EVENT_USER_REMOVE</td>
</tr>
<tr>
<td>GUILD_VOICE_STATES</td>
<td>128</td>
<td>VOICE_STATE_UPDATE</td>
</tr>
<tr>
<td>GUILD_WEBHOOKS</td>
<td>32</td>
<td>WEBHOOKS_UPDATE</td>
</tr>
<tr>
<td>MESSAGE_CONTENT*</td>
<td>32768</td>
<td>-</td>
</tr>
<tr>
<td>NONE</td>
<td>0</td>
<td>-</td>
</tr>
</tbody>
</table>
<ul>
<li>Intents marked with <code>*</code> are privilaged intents.</li>
</ul>

</details>

---

## REST and Cache implementation.

### What is REST?

A REST (REpresentational State Transfer) API is an interface that allows exchange of data from your application to a web service using HTTP requests (GET/POST/PATCH etc).

---

### Hikari's RESTClient

In the case of hikari, requests to the Discord RESTApi are handled by the [`hikari.api.RESTClient`](https://www.hikari-py.dev/hikari/api/rest.html#hikari.api.rest.RESTClient) class which can be accessed using `GatewayBot.rest`.

The RESTClient provides you with methods that can be utilized to send/fetch data payloads to/from discord API.

**Example Usage**

- Sending a message to some channel whenever someone joins a server.

```py
import hikari

intents = hikari.Intents(hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.GUILD_MEMBERS)
bot = hikari.GatewayBot("token", intents=intents)

CHANNEL_ID = 123456789


@bot.listen()
async def member_added(event: hikari.MemberCreateEvent) -> None:
    await bot.rest.create_message(  # bot.rest here is a RESTClient object.
        CHANNEL_ID, f"{event.member.username} Joined the server."
    )


bot.run()
```

**Explanation**

- Declaring a variable named `CHANNEL_ID` which stores the ID of the channel to send logs in.
- Creating a `hikari.MemberCreateEvent` which is fired when a new Member is added to a server.
- Inside the member_added listener, `bot.rest` is used to access the `hikari.api.RESTClient` object ...
- ... which has a `create_message` method used to send messages on discord.

You can find all the RESTClient methods [`here`](https://www.hikari-py.dev/hikari/api/rest.html#hikari.api.rest.RESTClient)

### Cache

Hikari has a clean and completely customizable Cache Implementation which the library uses to store discord objects states inside the bot process' memory.

**How is Cache helpful?**

Discord has strict rate limits for Bot applications, i.e. making too many requests to API can get your application temporary/permanently banned from using the API. The cache stores the object so you don't need to `fetch` them every time from the API to use them.

It can be accessed using `GatewayBot.cache` which returns a [`hikari.api.Cache`]() object with methods to work with the internal cache state.

**Example Usage**

- Getting the total number of Members in a server.

```py
import hikari

intents = hikari.Intents(
    hikari.Intents.ALL_UNPRIVILEGED
    | hikari.Intents.GUILD_MEMBERS # 1
    | hikari.Intents.MESSAGE_CONTENT # 1
)
bot = hikari.GatewayBot("token", intents=intents)


@bot.listen()
async def message_sent(event: hikari.GuildMessageCreateEvent) -> None:
    if event.content.startswith("!members"): # 2
        members = bot.cache.get_members_view_for_guild(event.message.guild_id) # 3
        await event.message.respond(f"This server has {len(members)} members.")


bot.run()
```

**Explanation**

- 1: `MESSAGE_CONTENT` intent is required to get the content of a message, else `None` is returned. `GUILD_MEMBERS` intents is required for cache-ing guild members.
- 2: Checking if the message content starts with the string we want as the command.
- 3: Getting all the members in the server as a dictionary as { member_id: hikari.Member } mapping.

---

## Command Handlers

Hikari does not have an inbuilt command handler, but you can pick from some commonly used ones for hikari:

- [hikari-lightbulb](https://github.com/tandemdude/hikari-lightbulb)
- [hikari-tanjun](https://github.com/FasterSpeeding/Tanjun)
- [hikari-crescent](https://github.com/magpie-dev/hikari-crescent)

**Given below are basic examples of how these command handlers work.**

---

### hikari-lightbulb

Lightbulb is an easy-to-use command handler with a simple interface and many other utils & extensions.

Github: [tandemdude/hikari-lightbulb](https://github.com/tandemdude/hikari-lightbulb/)

**Example command**

```py
import lightbulb
from hikari import Intents

intents = Intents(Intents.ALL_UNPRIVILEGED | Intents.MESSAGE_CONTENT)

# lightbulb.BotApp is a subclass of hikari.GatewayBot
bot = lightbulb.BotApp("token", "prefix", intents=intents)

# adding the command to bot
@bot.command
# adding information about the command
@lightbulb.command("ping", "replies with pong")
# mentioning the command type
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
# command callback
async def ping(context: lightbulb.Context) -> None:
    await context.respond("pong")


bot.run()
```

---

### hikari-crescent

An application-command-only command handler that allows you to make app commands using simple functions and classes.

Github: [magpie-dev/hikari-crescent](https://github.com/magpie-dev/hikari-crescent)

**Example Command**

```py
import crescent

bot = crescent.Bot("token")

# using command function


@bot.include  # adding the command to the bot
@crescent.command  # defining command type
async def ping(context: crescent.Context) -> None:  # callback
    await context.respond("Pong!")


# using classes


@bot.include
@crescent.command(name="echo")
class Echo:
    text = crescent.option(
        option_type=str, description="the text to send.", name="text"
    )

    async def callback(self, context: crescent.Context) -> None:  # callback function
        await context.respond(self.text)


bot.run()
```

---

### hikari-tanjun

A flexible command framework designed to extend Hikari.

It allows you to have more control over the workflow than the other command handlers.

Github: [FasterSpeeding/Tanjun](https://github.com/FasterSpeeding/Tanjun)

**Example Command**

```py
import hikari
import tanjun

# defining a GatewayBot for tanjun handler to use
gatewaybot = hikari.GatewayBot(
    "token",
    intents=hikari.Intents(
        hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT
    ),
)
client = tanjun.Client.from_gateway_bot(gatewaybot).add_prefix("prefix")

component = tanjun.Component(name="command component")
client.add_component(component)  # adding the component to bot.

# a simple message ping command
@component.with_command
@tanjun.as_message_command("ping")
async def ping(context: tanjun.abc.Context) -> None:
    await context.respond("pong!")


# a simple slash ping command
@component.with_command
@tanjun.as_slash_command("ping", "slash ping command")
async def ping_slash(context: tanjun.abc.Context) -> None:
    await context.respond("pong!")

# slash command with argument
@component.with_command
@tanjun.with_str_slash_option("text", "the text to send")
@tanjun.as_slash_command("echo", "repeats your text.")
async def echo(context: tanjun.abc.Context, text: str) -> None:
    await context.respond(text)


gatewaybot.run()
```
---

## Components

Hikari has support for components like Buttons, Select menus etc internally, which can also be extended using libraries like `hikari-miru` ( which we will talk about below. )

### Creating a basic Button with hikari.

* Buttons ( or any component) can be created using the [`ActionRowBuilder`](https://www.hikari-py.dev/hikari/impl/special_endpoints.html#hikari.impl.special_endpoints.ActionRowBuilder) class.

```py
import hikari

intents = hikari.Intents(
    hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT
)
bot = hikari.GatewayBot("token", intents=intents,)


@bot.listen()
async def send_buttons(event: hikari.MessageCreateEvent) -> None:
    if event.message.content == "!buttons":
        action_row = bot.rest.build_action_row() 
        action_row.add_button(hikari.ButtonStyle.PRIMARY, "my_button").set_label(
            "Click on me!"
        ).add_to_container()
        await event.message.respond("Here's a cool button!", component=action_row)
```

**Explanation**

* `bot.rest.build_action_row()` returns an `hikari.impl.special_endpoints.ActionRowBuilder` class.
* `action_row.add_button()` adds a button to the action-row, the first argument is the ButtonStyle, the second one is the custom id of the button.
* `set_label()` adds the label to the button i.e. the text that appears on the button interface.
* `add_to_container`, finally when the component is built, you can add it to the builder's container using this method.

And you have a Button ready here!

* To respond to the button when it's clicked you need to use `GatwayBot.wait_for` method which waits for an event to dispatch.

```py
        def check(e: hikari.InteractionCreateEvent) -> bool:
            return (
                isinstance(inter := e.interaction, hikari.ComponentInteraction)
                and inter.custom_id == "my_button"
            )

        try:
            response: hikari.InteractionCreateEvent = await bot.wait_for(
                hikari.InteractionCreateEvent, timeout=30, predicate=check
            )
            await message.edit(
                f"{response.interaction.user} clicked on the button", components=[]
            )
        except asyncio.TimeoutError:
            await message.edit("No one clicked on the button", components=[])


bot.run()
```

**Explanation**

* The `check` function makes sure that only the button we sent is getting clicked.
* `GatewayBot.wait_for` is used to wait for an event to get dispatched, it takes the event class as the first argument, along with timeout as a required argument and predicate which is our check function as an optional argument.
* An asyncio.TimeoutError is raised if the event mentioned is not dispatched with the conditions in the predicate within the time mentioned in the timeout

---

### hikari-miru

hikari-miru is a component handler for hikari based on discord.py views. It uses a similar syntax for building components with an easier interface.

Github: [`HyperGH/hikari-miru`](https://github.com/HyperGH/hikari-miru)

* miru example for the button example above 

```py
import hikari
import miru

intents = hikari.Intents(
    hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT
)
bot = hikari.GatewayBot("token", intents=intents,)
miru.load(bot)


class View(miru.View):
    async def on_timeout(self) -> None:
        await self.message.edit("No one clicked on the button", components=[])

    @miru.button(label="Click on me!")
    async def button_click(self, button: miru.Button, ctx: miru.Context) -> None:
        await ctx.edit_response(f"{ctx.user} clicked on the button.", components=[])


@bot.listen()
async def send_buttons(event: hikari.MessageCreateEvent) -> None:
    if event.message.content == "!buttons":
        view = View(timeout=30)
        message = await event.message.respond(
            "Here's a cool button!", components=view.build() # 1
        )
        view.start(message) # 2


bot.run()
```

**Explanation**

* `miru.load(bot)` loads the bot into the miru module which is utilized later for other functionalities
* Creating a `View` class, just like it is done with discord.py
* 1: While sending the view, it is important to call the `.build()` method, it converts the view to a list of `ActionRowBuilder`s.
* 2: For the view to listen to messages, it's important to pass the message in `view.start()` method.


---

## Other Important Info

### uvloop

You can get a performance boost by replacing the default asyncio event loop with `uvloop`.

**Note**: This works only in UNIX based system.

* Insalling uvloop using your package manager

```bash
$python -m pip install uvloop`
```

* Implementing uvloop for your project.
```py
import os

if os.name != "nt": # checking if the os is not windows.
    import uvloop
    uvloop.install()

```


### Embeds

Here's everything you can do with embeds.

#### Example Code

```py
import datetime
import hikari

embed = hikari.Embed(
    title="embed's title",
    description=" embed's description",
    color=0xFFFFFF,  # you can use any hikari.Colourish object here.
    timestamp=datetime.datetime.now().astimezone(),  # any datetime object
)  # all the argumnts provided to this constructor are optional.

# adding an author
# the icon can be any hikari.Resourceish object which includes User avatars, local files, attachments, bytes, etc.
embed.set_author(
    name="embed author name",
    url="https://the-author-url.com",
    icon="https://linktoimage.url",
)

# adding a footer
# the icon can be any hikari.Resourceish object which includes User avatars, local files, attachments, bytes, etc.
embed.set_footer(
    "the footer text, this can be a positional or keyword arg",
    icon="https://linktoimage.url",
)

# images and thumbnails
embed.set_image("https://linktoimage.url")  # any hikari.Resourceish object
embed.set_thumbnail("https://linktoimage.url")  # any hikari.Resourceish object

# add fields
embed.add_field(
    name="field name", value="field value"
)  # name and value are required arguments.

embed.title = "embed's"
embed.description = "'s property can be edited"
embed.author = hikari.EmbedAuthor(name="this way too")
embed.colour = 0x000000  # color is an alias of colour.
```
<details><summary><b>Embed visualization</b></summary>
<img src="https://raw.githubusercontent.com/sarthhh/hikari_guide/main/assets/embed.png" alt="embed structure">
</details>

---
