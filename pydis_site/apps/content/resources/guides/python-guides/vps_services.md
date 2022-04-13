---
title: Free Hosting Services for Discord Bots
description: "This article covers the disasdvantages of utilising a free hosting service to run a discord bot. Two commonly used services are discussed below. "
toc: 2
---



## Recommended VPS services

If you need to run your bot 24/7 (with no downtime), you should consider using a virtual private server (VPS). This is a list of VPS services that are sufficient for running Discord bots.

* Europe
    * [netcup](https://www.netcup.eu/)
        * Germany & Austria data centres.
        * Great affiliate program.
    * [Yandex Cloud](https://cloud.yandex.ru/)
        * Vladimir, Ryazan, and Moscow region data centres.
    * [Scaleway](https://www.scaleway.com/)
        * France data centre.
    * [Time 4 VPS](https://www.time4vps.eu/)
        * Lithuania data centre.
* US
    * [GalaxyGate](https://galaxygate.net/)
        * New York data centre.
        * Great affiliate program.
* Global
    * [Linode](https://www.linode.com/)
    * [Digital Ocean](https://www.digitalocean.com/)
    * [OVHcloud](https://www.ovhcloud.com/)
    * [Vultr](https://www.vultr.com/)


## Why not to use free hosting services for bots
While these may seem like nice and free services, it has a lot more caveats than you might think. For example, below discusses the drawbacks of using common free hosting services to host a discord bot.

### Replit

- The machines are super underpowered, resulting in your bot lagging a lot as it gets bigger.
- You need to run a webserver alongside your bot to prevent it from being shut off. This uses extra machine power.
- Repl.it uses an ephemeral file system. This means any file you saved through your bot will be overwritten when you next launch.

- They use a shared IP for everything running on the service.
This one is important - if someone is running a user bot on their service and gets banned, everyone on that IP will be banned. Including you.

### Heroku
- Bots are not what the platform is designed for. Heroku is designed to provide web servers (like Django, Flask, etc). This is why they give you a domain name and open a port on their local emulator.

- Heroku's environment is heavily containerized, making it significantly underpowered for a standard use case.

- Heroku's environment is volatile. In order to handle the insane amount of users trying to use it for their own applications, Heroku will dispose your environment every time your application dies unless you pay.

- Heroku has minimal system dependency control. If any of your Python requirements need C bindings (such as PyNaCl binding to libsodium, or lxml binding to libxml), they are unlikely to function properly, if at all, in a native environment. As such, you often need to resort to adding third-party buildpacks to facilitate otherwise normal CPython extension functionality. (This is the reason why voice doesn't work natively on heroku)

- Heroku only offers a limited amount of time on their free programme for your applications. If you exceed this limit, which you probably will, they'll shut down your application until your free credit resets.
