---
title: Setting Different Statuses on Your Bot
description: How to personalize your Discord bot status
---

You've probably seen a bot or two have a status message under their username in the member bar set to something such as `Playing Commands: .help`.

This guide shows how to set such a status, so your bot can have one as well.

**Please note:**

If you want to change the bot status, it is suggested to not do so during the `on_ready` event, since it would be called many times and making an API call on that event has a chance to disconnect the bot.

The status should not have a problem being set during runtime with `change_presence`, in the examples shown below.

Instead, set the desired status using the activity / status kwarg of commands.Bot, for example:
```python
bot = commands.Bot(command_prefix="!", activity=..., status=...)
```

The following are examples of what you can put into the `activity` keyword argument.

#### Setting 'Playing' Status
```python
await client.change_presence(activity=discord.Game(name="a game"))
```

#### Setting 'Streaming' Status
```python
await client.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))
```

#### Setting 'Listening' Status
```python
await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
```

#### Setting 'Watching' Status
```python
await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
```

### Add Optional Status as Well:

* `discord.Status.online` (default, green icon)
* `discord.Status.idle` (yellow icon)
* `discord.Status.do_not_disturb` (red icon)
* `discord.Status.offline` (gray icon)
