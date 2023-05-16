---
title: Subclassing Bot
description: "Subclassing the discord.py Bot class to add more functionality and customisability."
---

## Basic Subclassing
First, a [basic article](https://www.codesdope.com/course/python-subclass-of-a-class/) on subclassing will provide some fundamental knowledge, which is highly suggested before moving on to this topic, as subclassing [`Bot`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot) can ultimately be a complicated task.

## The benefits of subclassing bot
Subclassing Bot can be very beneficial as it provides you with more control and customisability of how your bot functions, also allowing you to add extra features, such as custom bot attributes or methods. For example, the default [Context](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Context) can be overriden to add more functionality.

You can subclass `commands.Bot` as shown below:
```python
class CustomBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        # Forward all arguments, and keyword-only arguments to commands.Bot
        super().__init__(*args, **kwargs)

        # Custom bot attributes can be set here.
        self.launch_time = datetime.datetime.utcnow()
        self.example_integer = 5

    # Here you are overriding the default start method and write your own code.
    async def start(self, *args, **kwargs) -> None:
        """Establish a database connection."""
        self.db = await aiosqlite.connect('sqlite.db')
        await super().start(*args, **kwargs)

    # Example of a custom bot method
    def status(self) -> str:
        """Get bot launch time in UTC and status."""
        return f"Bot started at {self.launch_time}, running."

# All arguments as passed to commands.Bot can be passed here.
bot = CustomBot(
    command_prefix="!",  # Prefix can be set to any string.
    # Discord intents, refer to https://discordpy.readthedocs.io/en/stable/intents.html
    intents=discord.Intents.default()  
)


# Example bot command
@bot.command()
async def ping(ctx):
    """
    Creates a command with the name `ping`.

    When invoked, sends `pong`.
    """
    await ctx.send("pong")


# Having the token as an environment variable is recommended.
# Refer to https://www.pythondiscord.com/pages/guides/python-guides/keeping-tokens-safe/
token = YOUR_TOKEN_HERE
bot.run(token)
```
With the above example, you are not required to change any of the existing or future code, it is identical to code done without subclassing bot.
