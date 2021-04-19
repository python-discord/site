---
title: Discord.py Learning Guide
description: A learning guide for the discord.py bot framework written by members of our community.
icon: fab fa-python
toc: 2
---

<!-- discord.py Badge -->
<a href="https://github.com/Rapptz/discord.py/">
    <div class="tags has-addons">
        <span class="tag is-dark">discord.py</span><span class="tag is-info">≥1.0</span>
    </div>
</a>

Interest in creating a Discord bot is a common introduction to the world of programming in our community.

Using it as your first project in programming while trying to learn is a double-edged sword.
A large number of concepts need to be understood before becoming proficient at creating a bot, making the journey of learning and completing the project more arduous than more simple projects designed specifically for beginners.
However in return, you get the opportunity to expose yourself to many more aspects of Python than you normally would and so it can be an amazingly rewarding experience when you finally reach your goal.

Another excellent aspect of building bots is that it has a huge scope as to what you can do with it, almost only limited by your own imagination.
This means you can continue to learn and apply more advanced concepts as you grow as a programmer while still building bots, so learning it can be a useful and enjoyable skillset.

This page provides resources to make the path to learning as clear and easy as possible, and collates useful examples provided by the community that may address common ideas and concerns that are seen when working on Discord bots.

## Essential References

Official Documentation: [https://discord.py.readthedocs.io](https://discordpy.readthedocs.io/)

Source Repository: [https://github.com/Rapptz/discord.py](https://github.com/Rapptz/discord.py)

## Creating a Discord Bot Account

1. Navigate to [https://discord.com/developers/applications](https://discord.com/developers/applications) and log in.
2. Click on `New Application`.
3. Enter the application's name.
4. Click on `Bot` on the left side settings menu.
5. Click `Add Bot` and confirm with `Yes, do it!`.

### Client ID
Your Client ID is the same as the User ID of your Bot.
You will need this when creating an invite URL.

You can find your Client ID located on the `General Information` settings page of your Application, under the `Name` field.

Your Client ID is not a secret, and does not need to be kept private.

### Bot Token

Your Bot Token is the token that authorises your Bot account with the API.
Think of it like your Bot's API access key.
With your token, you can interact with any part of the API that's available to bots.

You can find your Bot Token located on the Bot settings page of your Application, under the Username field.
You can click the Copy button to copy it without revealing it manually.

**Your Bot Token is a secret, and must be kept private.**
If you leak your token anywhere other people has access to see it, no matter the duration, you should reset your Bot Token.

To reset your token, go to the Bot settings page of your Application, and click the Regenerate button.
Be sure to update the token you're using for your bot script to this new one, as the old one will not work anymore.

### Permissions Integer

Discord Permissions are typically represented by a Permissions Integer which represents all the Permissions that have been allowed.

You can find a reference to all the available Discord Permissions, their bitwise values and their descriptions here:<br>
[https://discordapp.com/developers/docs/topics/permissions#permissions-bitwise-permission-flags](https://discordapp.com/developers/docs/topics/permissions#permissions-bitwise-permission-flags)

If you want to create your own Permissions Integer, you can generate it in the `Bot` settings page of your Application, located at the bottom of the page.

Tick the permissions you want to be allowing, and it'll update the `Permissions Integer` field, which you can use in your Bot Invite URL to set your bot's default permissions when users go to invite it.

### Bot Invite URL

Bot's cannot use a server invite link. Instead, they have to be invited by a member with the Manage Server permission.

The Bot Invite URL is formatted like:
`https://discordapp.com/oauth2/authorize?client_id={CLIENT_ID}&scope=bot&permissions={PERMISSIONS_INTEGER}`

You can create the Invite URL for your bot by replacing:

* `{CLIENT_ID}` with your [Client ID](#client-id)
* `{PERMISSIONS_INTEGER}` with the [Permissions Integer](#permissions-integer)

You can also generate it with the [Permissions Calculator](https://discordapi.com/permissions.html tool) tool.

## Using the Basic Client (`discord.Client`) { data-toc-label="Using the Basic Client" }

Below are the essential resources to read over to get familiar with the basic functionality of `discord.py`.

* [Basic event usage](https://discordpy.readthedocs.io/en/latest/intro.html#basic*concepts)
* [Simple bot walkthrough](https://discordpy.readthedocs.io/en/latest/quickstart.html#a*minimal*bot)
* [Available events reference](https://discordpy.readthedocs.io/en/latest/api.html#event*reference)
* [General API reference](https://discordpy.readthedocs.io/en/latest/api.html)

## Using the Commands Extension (`commands.Bot`) { data-toc-label="Using the Commands Extension" }

The Commands Extension has a explanatory documentation walking you through not only what it is and it's basic usage, but also more advanced concepts.
Be sure to read the prose documentation in full at:<br>
[https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html](https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html)

It fully covers:
* How to create bot using the Commands Extension
* How to define commands and their arguments
* What the Context object is
* Argument Converters
* Error Handling basics
* Command checks

You will also need to reference the following resources:
* [Commands Extension exclusive events](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#event-reference)
* [Commands Extension API reference](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html)

## FAQ

The documentation covers some basic FAQ's, and they are recommended to be read beforehand, and referenced before asking for help in case it covers your issue:
[https://discordpy.readthedocs.io/en/latest/faq.html](https://discordpy.readthedocs.io/en/latest/faq.html)

## Usage Examples

### Official Examples and Resources

The official examples can be found on the [source repository](https://github.com/Rapptz/discord.py/tree/master/examples).

The most commonly referenced examples are:

* [Basic Commands Extension Bot](https://github.com/Rapptz/discord.py/blob/master/examples/basic_bot.py)
* [Background Task Example](https://github.com/Rapptz/discord.py/blob/master/examples/background_task.py)

### Permissions Documentation

* [Role Management 101](https://support.discordapp.com/hc/en-us/articles/214836687-Role-Management-101)
* [Full Permissions Documentation](https://discordapp.com/developers/docs/topics/permissions)

### Community Examples and Resources

The `discord.py` developer community over time have shared examples and references with each other.<br>
The following are a collated list of the most referenced community examples.

#### Extensions / Cogs
* [Extension/Cog Example](https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be) - *Credit to EvieePy*
* [Available Cog Methods](https://gist.github.com/Ikusaba-san/69115b79d33e05ed07ec4a4f14db83b1) - *Credit to MIkusaba*

#### Error Handling
* [Decent Error Handling Example](https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612) - *Credit to EvieePy*

#### Embeds
* [Embed Live Designer and Visualiser](https://leovoel.github.io/embed-visualizer/) - *Credit to leovoel*
* [Embed Element Reference](https://cdn.discordapp.com/attachments/84319995256905728/252292324967710721/embed.png)<br>
![Embed Element Reference](/static/images/content/discordpy_embed.webp){: width="200" }

##### Using Local Images in Embeds
```py
filename = "image.png"

f = discord.File("some_file_path", filename=filename)
embed = discord.Embed()

embed.set_image(url=f"attachment://{filename}")
await messagable.send(file=f, embed=embed)
```

##### Embed Limits

| **Element** | **Characters** |
| -------------- | ---------------------- |
| Title | 256 |
| Field Name | 256 |
| Field Value | 1024 |
| Description | 2048 |
| Footer | 2048 |
| **Entire Embed** | **6000**

| **Element** | **Count** |
| -------------- | ---------------------- |
| Fields | 25 |

#### Emoji

- [Bot's Using Emoji](https://gist.github.com/scragly/b8d20aece2d058c8c601b44a689a47a0)

#### Activity Presence

- [Setting Bot's Discord Activity](https://gist.github.com/scragly/2579b4d335f87e83fbacb7dfd3d32828)

#### Image Processing

- [PIL Image Processing Example Cog](https://gist.github.com/Gorialis/e89482310d74a90a946b44cf34009e88) - *Credit to Gorialis*

### Systemd Service
**botname.service**<br>
```ini
[Unit]
Description=My Bot Name
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/your/bots/directory
ExecStart=/usr/bin/python3 /your/bots/directory/file.py
User=username
Restart=on-failure

[Install]
WantedBy=network-online.target
```

**Directory**<br>
`/usr/local/lib/systemd/system`

**Service Commands**<br>
Refresh systemd after unit file changes:<br>
`systemctl daemon-reload`

Set service to start on boot:<br>
`systemctl enable botname`

Start service now:<br>
`systemctl start botname`

Stop service:<br>
`systemctl stop botname`

**Viewing Logs**<br>
All logs:<br>
`journalctl -u botname`

Recent logs and continue printing new logs live:<br>
`journalctl -fu mybot`
