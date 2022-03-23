---
title: Custom Help Command
description: "Overwrite discord.py's help command to implement custom functionality"
---

First,  a [basic walkthrough](https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96) by Stella#2000 on subclassing the HelpCommand will provide some foundational knowledge required before attempting a more customizable help command.

---

## Custom Subclass of Help Command
If this does not fit your needs and you require a more customizable help command, you can subclass HelpCommand and add individual command details. Below is a basic demonstration:

```python
class MyHelpCommand(commands.HelpCommand):
    async def command_callback(self, ctx, *,command=None):
        if command:
            await ctx.send(f"This is the help page for the command {command} ")
        else:
            await ctx.send("This is the front page for the bots help command")
bot.help_command = MyHelpCommand()
```
---
You can handle when a user does not pass a command name when invoking the help command and make a fancy and customized embed; here a page that describes the bot and shows a list of commands is generally used, however if a command is passed in, you can display detailed information of the command. Below are references from the documentation below that can be utilised:

* [Get the command object](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.get_command)

* [Get the command name](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command.name)

* [Get the command aliases](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command.aliases)

* [Get the command brief](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command.brief)

* [Get the command usage](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command.usage)

* Get the command cooldown - `command_object._buckets._cooldown.per`
