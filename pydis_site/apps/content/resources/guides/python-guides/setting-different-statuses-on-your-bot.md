---
title: Setting Different Statuses to Set Your Bot
description: How to personalize your Discord bot status
---
**Different Statuses to Set Your Bot:**
```python
# Setting 'Playing' status
await client.change_presence(activity=discord.Game(name="a game"))
```
```python
# Setting 'Streaming' status
await client.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))
```
```python
# Setting 'Listening' status
await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
```
```python
# Setting 'Watching' status
await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
```

**Add Optional Status as Well:**
```python
status=discord.Status.<status>
```
**Available Statuses:**
```python
do_not_disturb (red icon)
```
```python
idle (yellow icon)
```
```python
online (default, green icon)
```
```python
offline (gray icon)
```
