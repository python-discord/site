---
title: Custom Help Command
description: "Overwrite discord.py's help command to implement custom functionality"
---

First, a basic walkthrough can be found [here](https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96) by Stella#2000 on subclassing the HelpCommand. It will provide some foundational knowledge that is required before attempting a more customizable help command.

## Custom Subclass of Help Command
If the types of classes of the HelpCommand do not fit your needs, you can subclass HelpCommand and use the class mehods to customize the output. Below is a simple demonstration using the following methods that can also be found on the documenation:

- [filter_commands](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.HelpCommand.filter_commands)

- [send_group_help](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.HelpCommand.send_bot_help)

- [send_command_help](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.HelpCommand.send_command_help)

- [send_group_help](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.HelpCommand.send_group_help)

- [send_error_message](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.HelpCommand.send_error_message)

```python
class MyHelp(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        """
        This is triggered when !help is invoked.

        This example demonstrates how to list the commands that the member invoking the help command can run.
        """
        filtered = await self.filter_commands(self.context.bot.commands, sort=True) # returns a list of command objects
        names = [command.name for command in filtered] # iterating through the commands objects getting names
        available_commands = "\n".join(names) # joining the list of names by a new line
        embed  = disnake.Embed(description=available_commands)
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        """This is triggered when !help <command> is invoked."""
        await self.context.send("This is the help page for a command")
        
    async def send_group_help(self, group):
        """This is triggered when !help <group> is invoked."""
        await self.context.send("This is the help page for a group command")

    async def send_cog_help(self, cog):
        """This is triggered when !help <cog> is invoked."""
        await self.context.send("This is the help page for a cog")

    async def send_error_message(self, error):
        """If there is an error, send a embed containing the error."""
        channel = self.get_destination() # this defaults to the command context channel
        await channel.send(error)

bot.help_command = MyHelp()
```

You can handle when a user does not pass a command name when invoking the help command and make a fancy and customized embed; here a page that describes the bot and shows a list of commands is generally used. However if a command is passed in, you can display detailed information of the command. Below are references from the documentation below that can be utilised:

- [Get the command object](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.get_command)

- [Get the command name](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command.name)

- [Get the command aliases](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command.aliases)

- [Get the command brief](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command.brief)

- [Get the command usage](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command.usage)
