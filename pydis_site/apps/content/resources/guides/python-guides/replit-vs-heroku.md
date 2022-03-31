---
title: Replit vs Heroku
description: A small comparisation between Replit and Heroku.
---

__**Replit**__
While this may seem like a nice and free service, it has a lot more caveats than you might think, such as:

- The machines are super underpowered.
- - This means your bot will lag a lot as it gets bigger.
- You need to run a webserver alongside your bot to prevent it from being shut off.
- - This isn't a trivial task, and eats more of the machines power.
- Repl.it uses an ephemeral file system.
- - This means any file you saved via your bot will be overwritten when you next launch.

- They use a shared IP for everything running on the service.
This one is important - if someone is running a user bot on their service and gets banned, everyone on that IP will be banned. Including you.

__**Heroku**__
- Bots are not what the platform is designed for. Heroku is designed to provide web servers (like Django, Flask, etc). This is why they give you a domain name and open a port on their local emulator.

- Heroku's environment is heavily containerized, making it significantly underpowered for a standard use case.

- Heroku's environment is volatile. In order to handle the insane amount of users trying to use it for their own applications, Heroku will dispose your environment every time your application dies unless you pay.

- Heroku has minimal system dependency control. If any of your Python requirements need C bindings (such as PyNaCl binding to libsodium, or lxml binding to libxml), they are unlikely to function properly, if at all, in a native environment. As such, you often need to resort to adding third-party buildpacks to facilitate otherwise normal CPython extension functionality. (This is the reason why voice doesn't work natively on heroku.)

- Heroku only offers a limited amount of time on their free programme for your applications. If you exceed this limit, which you probably will, they'll shut down your application until your free credit resets.