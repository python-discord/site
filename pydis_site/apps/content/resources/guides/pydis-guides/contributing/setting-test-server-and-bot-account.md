---
title: Setting Up a Test Server and Bot Account
description: How to get started with testing our bots.
icon: fab fa-discord
---

## Setting up a Test Server

1. Create a Discord Server if you haven't got one already to use for testing.

---

## Setting up a Bot Account

1. Go to the [Discord Developers Portal](https://discordapp.com/developers/applications/).
2. Click on the `New Application` button, enter your desired bot name, and click `Create`.
3. In your new application, go to the `Bot` tab, click `Add Bot`, and confirm `Yes, do it!`
4. Change your bot's `Public Bot` setting off so only you can invite it, save, and then get your **Bot Token** with the `Copy` button.
> **Note:** **DO NOT** post your bot token anywhere public, or it can and will be compromised.
5. Save your **Bot Token** somewhere safe to use in the project settings later.
6. In the `OAuth2` tab, grab the **Client ID**.
7. Replace `<CLIENT_ID_HERE>` in the following URL and visit it in the browser to invite your bot to your new test server.
```plaintext
https://discordapp.com/api/oauth2/authorize?client_id=<CLIENT_ID_HERE>&permissions=8&scope=bot
```
---

## Obtain the IDs

First, enable developer mode in your client so you can easily copy IDs.

1. Go to your `User Settings` and click on the `Appearance` tab.
2. Under `Advanced`, enable `Developer Mode`.

#### Guild ID

Right click the server icon and click `Copy ID`.

#### Channel ID

Right click a channel name and click `Copy ID`.

#### Role ID

Right click a role and click `Copy ID`.
The easiest way to do this is by going to the role list in the guild's settings.

#### Emoji ID

Insert the emoji into the Discord text box, then add a backslash `\`  right before the emoji and send the message.
The result should be similar to the following

```plaintext
<:bbmessage:511950877733552138>
```

The long number you see, in this case `511950877733552138`, is the emoji's ID.

#### Webhook ID

Once a [webhook](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks) is created, the ID is found in the penultimate part of the URL.
For example, in the following URL, `661995360146817053` is the ID of the webhook.

```plaintext
https://discordapp.com/api/webhooks/661995360146817053/t-9mI2VehOGcPuPS_F8R-6mB258Ob6K7ifhtoxerCvWyM9VEQug-anUr4hCHzdbhzfbz
```
