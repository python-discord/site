---
title: Configure Environment Variables
description: A guide to configuring environment variables.
icon: fas fa-cog
---

1. Create a text file named **.env** in your project root (that's the base folder of your repository):
    * Unix/Git Bash: `touch /path/to/project/.env`
    * Windows CMD: `type nul > \path\to\project\.env` (The error *The system cannot find the file specified* can be safely ignored.)
> **Note:** The entire file name is literally `.env`
2. Open the file with any text editor.
3. Each environment variable is on its own line, with the variable and the value separated by a `=` sign.

Example:

* Set the environment variable `SEASONALBOT_DEBUG` to `True`:
```
SEASONALBOT_DEBUG=True
```
* Set the environment variable `CHANNEL_ANNOUNCEMENTS` to `12345`:
```
CHANNEL_ANNOUNCEMENTS=12345
```
