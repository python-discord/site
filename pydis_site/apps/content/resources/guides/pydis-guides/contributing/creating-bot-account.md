---
title: Setting up a Bot Account
description: How to set up a bot account.
icon: fab fa-discord
---
1. Go to the [Discord Developers Portal](https://discordapp.com/developers/applications/).
2. Click on the `New Application` button, enter your desired bot name, and click `Create`.
3. In your new application, go to the `Bot` tab, click `Add Bot`, and confirm `Yes, do it!`
4. Change your bot's `Public Bot` setting off so only you can invite it, save, and then get your **Bot Token** with the `Copy` button.
> **Note:** **DO NOT** post your bot token anywhere public, or it can and will be compromised.
5. Save your **Bot Token** somewhere safe to use in the project settings later.
6. In the `General Information` tab, grab the **Client ID**.
7. Replace `<CLIENT_ID_HERE>` in the following URL and visit it in the browser to invite your bot to your new test server.
```plaintext
https://discordapp.com/api/oauth2/authorize?client_id=<CLIENT_ID_HERE>&permissions=8&scope=bot
```
Optionally, you can generate your own invite url in the `OAuth` tab, after selecting `bot` as the scope.