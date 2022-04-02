---
title: Fix SSL certificate error.
description: A guide about how to fix the SSL certificate error.
---
**How to fix SSL Certificate issue on Windows**

Firstly, try updating your OS, wouldn't hurt to try.
Now, if you're still having an issue, you would need to download the certificate for the SSL.
The SSL Certificate, Sectigo (cert vendor) provides a download link of certificate:
**https://crt.sh/?id=2835394**
You should find it at the bottom left corner, where its saying Download Certificate: __PEM__
Here's a picture of that if you can't find it: 
https://media.discordapp.net/attachments/336642776609456130/776070065694048276/s6ONfwUye1.png

You have to setup certificate yourself, you can just click on it, or if that doesn't work, refer here:
https://portal.threatpulse.com/docs/sol/Solutions/ManagePolicy/SSL/ssl_chrome_cert_ta.htm

**How to fix SSL Certificate issue on Mac**

Navigate to your Applications/Python 3.x/ folder and double click the Install Certificates.command to fix this.
That's it!
Happy coding!

For those curious, it was caused by this:
https://support.sectigo.com/Com_KnowledgeDetailPage?Id=kA03l00000117LT 
