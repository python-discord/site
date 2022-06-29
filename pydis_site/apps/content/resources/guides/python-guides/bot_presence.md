---
title: Setting different bot presences
description: In depth tutorial on how to set all available presence to your bot!
---
![image](https://cdn.discordapp.com/attachments/847979818444521582/989739880449994772/unknown.png)

## Activities
1. Listening to ...

2. Playing ...

3. Streaming ...

4. Watching ...

5. Competing in ...



# Where should I change my bot's presence and when?

---

The presence can only be changed when your bot is connected to the Discord gateway. This is because it needs to send a `PRESENCE` gateway event but most libraries allow you to set the application's presence within the bot constructor!

## How do I get these statuses and activities for my bot?

---

Discord.py examples
=======
All discord.py **status** types can be found [here](https://discordpy.readthedocs.io/en/stable/api.html?highlight=status#discord.Status). All discord.py **activity** types can be found [here](https://discordpy.readthedocs.io/en/stable/api.html?highlight=discord%20activity#discord.ActivityType).

Online
-----
```py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="<Your prefix>", status=discord.Status.online)
```

Invisible/offline
-----
```py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="<Your prefix>", status=discord.Status.invisible)
```

Do not disturb
-----
```py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="<Your prefix>", status=discord.Status.dnd)
```
Idle
-----
```py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="<Your prefix>", status=discord.Status.idle)
```
Playing activity
-----
```py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="<Your prefix>", status=discord.Status.online, activity=discord.Game(name="with wumpus"))
```
Streaming activity
-----
```py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="<Your prefix>", status=discord.Status.online, activity=discord.Streaming(name="Wumpus Stream", url="the streams url"))
```

Listening activity
-----
```py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="<Your prefix>", status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="The wumpus song"))
```

Watching activity
-----
```py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="<Your prefix>", status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="The wumpus movie"))
```

Competing activity
-----
```py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="<Your prefix>", status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.competing, name="The wumpus competition"))
```

You can also change your bots presence after logging.
-----
You can also use the [change_presence](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=bot#discord.ext.commands.Bot.change_presence). method

> **_NOTE:_** The method should not be used inside of **on_ready()** as this event can be triggered multiple times after logging in. Resulting in sending multiple of the same `PRESENCE` gateway event payload to the gateway.

# Changing activity after a certain period of time!

---

A large number of bots having presences that change by themselves after a certain period. In discord.py this can be done using a task loop. You can read more about tasks [here](https://discordpy.readthedocs.io/en/latest/ext/tasks/index.html).

## An example to using changing activity!

```python
import discord
from discord.ext import commands, tasks
import random

bot = commands.Bot(command_prefix="<Your prefix>")

bot.changeable_activites = ("Call of Duty: Warzone", "Fall Guys", "Fortnite", "Call of Duty: Black Ops IV", "Sea of Thieves", "League of Legends", "Valorant")

@tasks.loop(minutes=2)
async def change_activity():
    await bot.wait_until_ready()
    new_activity = random.choice(bot.changeable_activites)
    await bot.change_presence(activity=discord.Game(new_activity))

change_activity.start()
```

# FAQ

#### Do discord.py forks also follow the same structure for changing presences?
- Yes, popular discord.py forks such as `disnake`, `nextcord` and `py-cord` also follow the same structure!

#### What is the minimum duration after which I should change the presence?
- A gap of `75 seconds` is ideal to change the presence of a bot.

#### Can I change my presence after every 5 seconds or so?
- The simple answer is **yes**. The better answer is **no** as spamming gateway event payloads to the gateway can result your bot in getting rate-limited from the discord API.

Credits
-----
[okimii#0434](https://discord.com/users/637458038915203127)
[Ashley V#0871](https://discord.com/users/925079016174682213)
