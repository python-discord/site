---
title: Keeping Discord Bot Tokens Safe
description: How to keep your bot tokens safe and safety measures you can take.
---
It's **very** important to keep a bot token safe, primarily because anyone who has the bot token can do whatever they want with the bot -- such as destroying servers your bot has been added to and getting your bot banned from the API.

# How to Avoid Leaking your Token
To help prevent leaking your token, you should ensure that you don't upload it to an open source program/website, such as replit and github, as they show your code publicly. The best practice for storing tokens is generally utilising .env files ([click here](https://vcokltfre.dev/tips/tokens/.) for more information on storing tokens safely)

# What should I do if my token does get leaked?

If for whatever reason your token gets leaked, you should immediately follow these steps:
- Go to the list of [Discord Bot Applications](https://discord.com/developers/applications) you have and select the bot application that had the token leaked.
- Select the Bot (1) tab on the left-hand side, next to a small image of a puzzle piece. After doing so you should see a small section named TOKEN (under your bot USERNAME and next to his avatar image)
- Press the Regenerate option to regen your bot token.

![Steps to Take to Reset your Discord Bot](https://media.discordapp.net/attachments/859123972884922418/966504639421894697/bot_application.jpg?width=1348&height=671)

Following these steps will create a new token for your bot, making it secure again and terminating any connections from the leaked token.

# Summary
Make sure you keep your token secure by storing it safely, not sending it to anyone you don't trust, and regenerating your token if it does get leaked.