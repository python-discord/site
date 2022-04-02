---
title: Setting Different Statuses to Set Your Bot
description: How to personalize your Discord bot status
---

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
