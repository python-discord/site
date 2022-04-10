---
title: Setting Different Statuses to Set Your Bot
description: How to personalize your Discord bot status
---
**Please note:**

If you want to change the bot status, it is suggested to not do it during the on_ready event, since it would be called
many times and making an API call on that event has a chance to disconnect the bot.
Instead, set the desired status using the  activity / status kwarg of commands.Bot, for example
`bot = commands.Bot(command_prefix="!", activity=..., status=...)`

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

#### Add Optional Status as Well:

* status=discord.Status.\<status>

####Available Statuses:

* do_not_disturb(red icon)


* idle(yellow icon)


* online(default, green icon)


* offline(gray icon)
