---
title: Fixing an SSL Certificate Error.
description: A guide on fixing an SSL certificate error.
---
#### How to fix SSL Certificate issue on Windows

Firstly, try updating your OS, wouldn't hurt to try.
Now, if you're still having an issue, you would need to download the certificate for the SSL.
The SSL Certificate, Sectigo (cert vendor) provides a download link of [certificate](https://crt.sh/?id=2835394)
You should find it at the bottom left corner, where it's saying Download Certificate: *PEM*
A picture where to find the certificate in the website is:
![location of certificate](https://media.discordapp.net/attachments/336642776609456130/776070065694048276/s6ONfwUye1.png)

You have to setup the certificate yourself. To do that you can just click on it, or if that doesn't work, refer [here]
(https://portal.threatpulse.com/docs/sol/Solutions/ManagePolicy/SSL/ssl_chrome_cert_ta.htm).

#### How to fix SSL Certificate issue on Mac

Navigate to your `Applications/Python 3.x/` folder and double click the `Install Certificates.command` to fix this.
