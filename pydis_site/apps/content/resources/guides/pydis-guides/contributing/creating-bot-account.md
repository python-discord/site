---
title: Setting up a Bot Account
description: How to set up a bot account.
icon: fab fa-discord
---
1. Go to the [Discord Developers Portal](https://discord.com/developers/applications).
1. Click on the `New Application` button, enter your desired bot name, and click `Create`.
1. In the `Installation` tab, set `Install Link` to `None` and click `Save Changes`.
1. In the `Bot` tab:

    - Turn off the `Public Bot` setting.
    - Turn on the `Message Content Intent` setting.
    - If setting up Python Bot, also turn on the `Server Members Intent` setting.
    - ...and click `Save Changes`.

1. Click the `Reset Token` button and then `Copy` the generated token. Save it somewhere safe, as you will need it later.

    **Note**: Do not post this token anywhere public, as it grants complete control of your bot.
    {: .notification .is-warning }

1. In the  `OAuth2` tab, select the `bot` scope and `Administrator` permission, and visit the generated URL in your Discord app or browser to invite the bot to your server.
