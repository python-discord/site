---
title: Preparing Your Hosts file
description: How to setup your hosts file for project usage.
icon: fas fa-cog
---

# What's a hosts file?
The hosts file maps a hostname/domain to an IP address, allowing you to visit a given domain on your browser and have it resolve by your system to the given IP address, even if it's pointed back to your own system or network.

When staging a local [Site](https://pythondiscord.com/pages/contributing/site/) project, you will need to add some entries to your hosts file so you can visit the site with the domain `http://pythondiscord.local`

# What to add
You would add the following entries to your hosts file.

```plaintext
127.0.0.1   pythondiscord.local
127.0.0.1   api.pythondiscord.local
127.0.0.1   staff.pythondiscord.local
127.0.0.1   admin.pythondiscord.local
```

# How to add it

### Linux
1. Run `sudo nano /etc/hosts`
2. Enter your user password.
3. Add the new content at the bottom of the file.
4. Use `CTRL+X`
5. Enter `y` to save.

_This covers most linux distributions that come with `nano`, however you're welcome to use whatever CLI text editor you're comfortable with instead._

### Windows
1. Open Notepad as Administrator.
2. Open the file `C:\Windows\System32\Drivers\etc\hosts`
3. Add the new content at the bottom of the file.
4. Save.

### MacOS
1. Run `sudo nano /private/etc/hosts` in Terminal.
2. Enter your user password.
3. Add the new content at the bottom of the file.
4. Use `CTRL+X`
5. Enter `y` to save.
6. Flush your DNS by running `dscacheutil -flushcache`
