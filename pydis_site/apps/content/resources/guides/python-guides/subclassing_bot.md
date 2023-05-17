---
title: Subclassing Bot
description: "Subclassing the discord.py `Bot` class to add more functionality and customizability."
---

## Basic Subclassing
First, a [basic article](https://www.codesdope.com/course/python-subclass-of-a-class/) on subclassing will provide some fundamental knowledge, which is highly suggested before moving on to this topic, as subclassing [`Bot`](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot) can ultimately be a complicated task.

## The Benefits of Subclassing Bot
Subclassing `Bot` can be very beneficial as it provides you with more control and customizability of how your bot functions, also allowing you to add extra features, such as custom bot attributes or methods. For example, the default [Context](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Context) can be [overridden](../discordpy-subclassing-context.md) to add more functionality.

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
    def get_launch_time_str(self) -> str:
        """Get bot launch datetime without milliseconds in UTC and status."""
        return f"Bot started at: {self.launch_time.strftime('%F %T')} UTC."

# All arguments as passed to commands.Bot can be passed here.
bot = CustomBot(
    command_prefix="!",  # Prefix can be set to any string.
    # Discord intents, refer to https://discordpy.readthedocs.io/en/stable/intents.html
    intents=discord.Intents.default()  
)


# Example bot command
@bot.command()
async def start_time(ctx):
    """
    Creates a command with the name `start_time`.

    When invoked, sends the output of the custom method `get_launch_time_str`.
    """
    await ctx.send(bot.get_launch_time_str())


# Having the token as an environment variable is recommended.
# Refer to https://www.pythondiscord.com/pages/guides/python-guides/keeping-tokens-safe/
token = YOUR_TOKEN_HERE
bot.run(token)
```
The next step would be to look into discord.py cogs as they help in organizing collections  of commands into various files and folders. Refer to [the official docs](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) for more on them.
