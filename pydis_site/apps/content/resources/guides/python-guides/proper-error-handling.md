---
title: Proper error handling in discord.py
description: Are you not getting any errors? This might be why!
---
If you're not recieving any errors in your console, even though you know you should be, try this:

# With bot subclass:
```py
import discord
from discord.ext import commands

import traceback
import sys

class MyBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_command_error(self, ctx: commands.Context, error):
        # Handle your errors here
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("I could not find member '{error.argument}'. Please try again")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"'{error.param.name}' is a required argument.")
        else:
            # All unhandled errors will print their original traceback
            print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

bot = MyBot(command_prefix="!", intents=discord.Intents.default())

bot.run("token")
```

# Without bot subclass
```py
import discord
from discord.ext import commands

import traceback
import sys

async def on_command_error(self, ctx: commands.Context, error):
    # Handle your errors here
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("I could not find member '{error.argument}'. Please try again")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"'{error.param.name}' is a required argument.")
    else:
        # All unhandled errors will print their original traceback
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
bot.on_command_error = on_command_error

bot.run("token")
```


Make sure to import `traceback` and `sys`!

-------------------------------------------------------------------------------------------------------------

Useful Links:
- [FAQ](https://discordpy.readthedocs.io/en/latest/faq.html)
- [Simple Error Handling](https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612)
