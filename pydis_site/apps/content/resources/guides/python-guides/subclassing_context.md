---
title: Subclassing Context
description: "Subclassing the default `commands.Context` class to add more functionability and customisability."
---

Start by reading the guide on [subclassing the `Bot` class](./subclassing_bot.md). A subclass of Bot has to be used to
inject your custom context subclass into discord.py.

## Overview

The way this works is by creating a subclass of discord.py's [`Context` class](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Context)
adding whatever functionality you wish. Usually this is adding custom methods or properties, so that you don't need to
copy it around or awkwardly import it elsewhere.

This guide will show you how to add a `prompt()` method to the context and how to use it in a command.

## Example subclass and code

The first part - of course - is creating the actual context subclass. This is done similarly to creating a bot
subclass, it will look like this:

```python
from typing import Optional

from discord import RawReactionActionEvent
from discord.ext import commands


class CustomContext(commands.Context):
    async def prompt(
            self,
            message: str,
            *,
            timeout=30.0,
            delete_after=True
    ) -> Optional[bool]:
        """Prompt the author with an interactive confirmation message.

        This method will send the `message` content, and wait for max `timeout` seconds
        (default is `30`) for the author to react to the message.

        If `delete_after` is `True`, the message will be deleted before returning a
        boolean or None (if the author didn't respond) indicating whether the author
        confirmed or denied.
        """
        msg = await self.send(message)

        for reaction in ('\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}'):
            await msg.add_reaction(reaction)

        confirmation = None

        def check(payload: RawReactionActionEvent):
            # 'nonlocal' works almost like 'global' except for functions inside of
            # functions. This means that when 'confirmation' is changed, that will
            # apply to the variable above
            nonlocal confirmation

            if payload.message_id != msg.id or payload.user_id != self.author.id:
                return False

            emoji = str(payload.emoji)

            if emoji == '\N{WHITE HEAVY CHECK MARK}':
                confirmation = True
                return True

            elif emoji == '\N{CROSS MARK}':
                confirmation = False
                return True

            # This means that it was neither of the two emojis added, so the author
            # added some other unrelated reaction.
            return False

        try:
            await self.bot.wait_for('raw_reaction_add', check=check, timeout=timeout)
        except asyncio.TimeoutError:
            # The 'confirmation' variable is still None in this case
            pass

        if delete_after:
            await msg.delete()

        return confirmation
```

After creating your context subclass, you need to override the `get_context()` method on your
Bot class and change the default of the `cls` parameter to this subclass:

```python
from discord.ext import commands


class CustomBot(commands.Bot):
    async def get_context(self, message, *, cls=CustomContext):  # From the above codeblock
        return await super().get_context(message, cls=cls)
```

Now that discord.py is using your custom context, you can use it in a command. For example:

```python
from discord.ext import commands


bot = CustomBot(...)  # Replace with the arguments for the bot


@bot.command()
async def massban(ctx: CustomContext, members: commands.Greedy[discord.Member]):
    if not await ctx.prompt(f"Are you sure you want to ban {len(members)}?"):
        # Return if the author cancelled, or didn't react
        return

    ...  # Perform the mass-ban, knowing the author has confirmed this action
```
