---
title: Discord Embed Limits
description: A guide that shows the limits of embeds in Discord and how to avoid them.
---

If you plan on using embed responses for your bot you should know the limits of the embeds on Discord or you will get `Invalid Form Body` errors:

- Embed **title** is limited to **256 characters**
- Embed **description** is limited to **4096 characters**
- An embed can contain a maximum of **25 fields**
- A **field name/title** is limited to **256 character** and the **value of the field** is limited to **1024 characters**
- Embed **footer** is limited to **2048 characters**
- Embed **author name** is limited to **256 characters**
- The **total of characters** allowed in an embed is **6000**

Now if you need to get over this limit (for example for a help command), you would need to use pagination.
There are several ways to do that:

- A library called `disputils` -> <https://pypi.org/project/disputils>
- An experimental library made by the discord.py developer called `discord-ext-menus` -> <https://github.com/Rapptz/discord-ext-menus>
- Make your own setup using the `wait_for()` and wait for a reaction to be added -> <https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.Bot.wait_for>
