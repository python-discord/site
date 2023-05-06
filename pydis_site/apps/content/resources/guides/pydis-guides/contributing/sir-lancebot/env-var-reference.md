---
title: Sir-Lancebot Environment Variable Reference
description: The full environment variable reference for Sir-Lancebot.
toc: 2
---
## General Variables
The following variables are needed for running Sir Lancebot:

| Environment Variable               | Description                                                                                |
|------------------------------------|--------------------------------------------------------------------------------------------|
| `CLIENT_TOKEN`                     | Bot Token from the [Discord developer portal](https://discord.com/developers/applications) |
| `CLIENT_GUILD`                     | ID of the Discord Server                                                                   |
| `ROLES_ADMINS`                     | ID of the role `@Admins`                                                                   |
| `ROLES_HELPERS`                    | ID of the role `@Helpers`                                                                  |
| `CHANNELS_ANNOUNCEMENTS`           | ID of the `#announcements` channel                                                         |
| `CHANNELS_DEVLOG`                  | ID of the `#dev-log` channel                                                               |
| `CHANNELS_SIR_LANCEBOT_PLAYGROUND` | ID of the `#sir-lancebot-commands` channel                                                 |
| `CHANNELS_REDDIT`                  | ID of the `#reddit` channel                                                                |

---
## Debug Variables
Additionally, you may find the following environment variables useful during development:

| Environment Variable       | Description                                                                                                |
|----------------------------|------------------------------------------------------------------------------------------------------------|
| `CLIENT_DEBUG`             | Debug mode of the bot                                                                                      | False |
| `CLIENT_PREFIX`            | The bot's invocation prefix                                                                                | `.` |
| `BRANDING_CYCLE_FREQUENCY` | Amount of days between cycling server icon                                                                 | 3 |
| `CLIENT_MONTH_OVERRIDE`    | Integer in range `[0, 12]`, overrides current month w.r.t. seasonal decorators                             |
| `REDIS_HOST`               | The address to connect to for the Redis database.                                                          |
| `REDIS_PORT`               | The port on which the Redis database is exposed.                                                           |
| `REDIS_PASSWORD`           | The password to connect to the Redis database.                                                             |
| `REDIS_USE_FAKEREDIS`      | If the FakeRedis module should be used. Set this to true if you don't have a Redis database setup.         |
| `BOT_SENTRY_DSN`           | The DSN of the sentry monitor.                                                                             |
| `TRASHCAN_EMOJI`           | The full emoji to use for the trashcan. Format should be like the output of sending `\:emoji:` on discord. |

---
## Tokens/APIs
If you will be working with an external service, you might have to set one of these tokens:

| Token                       | Description                                                                                                              |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------|
| `TOKENS_GITHUB`             | Personal access token for GitHub, raises rate limits from 60 to 5000 requests per hour.                                  |
| `TOKENS_GIPHY`              | Required for API access. [Docs](https://developers.giphy.com/docs/api)                                                   |
| `REDDIT_CLIENT_ID`          | OAuth2 client ID for authenticating with the [reddit API](https://github.com/reddit-archive/reddit/wiki/OAuth2).         |
| `REDDIT_SECRET`             | OAuth2 secret for authenticating with the reddit API. *Leave empty if you're not using the reddit API.*                  |
| `REDDIT_WEBHOOK`            | Webhook ID for Reddit channel                                                                                            |
| `TOKENS_YOUTUBE`            | An OAuth Key or Token are required for API access. [Docs](https://developers.google.com/youtube/v3/docs#calling-the-api) |
| `TOKENS_TMDB`               | Required for API access. [Docs](https://developers.themoviedb.org/3/getting-started/introduction)                        |
| `TOKENS_NASA`               | Required for API access. [Docs](https://api.nasa.gov/)                                                                   |
| `WOLFRAM_KEY`               | Required for API access. [Docs](https://products.wolframalpha.com/simple-api/documentation)                              |
| `TOKENS_UNSPLASH`           | Required for API access. Use the `access_token` given by Unsplash. [Docs](https://unsplash.com/documentation)            |
| `TOKENS_IGDB_CLIENT_ID`     | OAuth2 client ID for authenticating with the [IGDB API](https://api-docs.igdb.com/)                                      |
| `TOKENS_IGDB_CLIENT_SECRET` | OAuth2 secret for authenticating with the IGDB API. *Leave empty if you're not using the IGDB API.*                      |

---
## Seasonal Cogs
These variables might come in handy while working on certain cogs:

| Cog        | Environment Variable      | Description                                                     |
|------------|---------------------------|-----------------------------------------------------------------|
| Valentines | `ROLES_LOVEFEST`          | ID of the role `@Lovefest`                                      |
| Wolfram    | `WOLFRAM_USER_LIMIT_DAY`  | The amount of requests a user can make per day                  |
| Wolfram    | `WOLFRAM_GUILD_LIMIT_DAY` | The amount of requests that can come from the say guild per day |
