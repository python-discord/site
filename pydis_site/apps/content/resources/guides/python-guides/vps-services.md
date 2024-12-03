---
title: VPS and Free Hosting Service for Discord bots
description: This article lists recommended VPS services and covers the disasdvantages of utilising a free hosting service to run a discord bot.
toc: 2
---

## Recommended VPS services

If you need to run your bot 24/7 (with no downtime), you should consider using a virtual private server (VPS). Here is a list of VPS services that are sufficient for running Discord bots.

* Europe
    * [netcup](https://www.netcup.eu/?ref=177518)
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


## Why not to use free hosting services for bots?
While these may seem like nice and free services, it has a lot more caveats than you may think. For example, the drawbacks of using common free hosting services to host a discord bot are discussed below.

### Replit

- The machines are super underpowered, resulting in your bot lagging a lot as it gets bigger.

- You need to run a webserver alongside your bot to prevent it from being shut off. This uses extra machine power.

- Repl.it uses an ephemeral file system. This means any file you saved through your bot will be overwritten when you next launch.

- They use a shared IP for everything running on the service.
This one is important - if someone is running a user bot on their service and gets banned, everyone on that IP will be banned. Including you.
