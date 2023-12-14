---
title: Fixing an SSL Certificate Verification Error
description: A guide on fixing verification of an SSL certificate.
---

We're fixing the error Python specifies as [ssl.SSLCertVerificationError](https://docs.python.org/3/library/ssl.html#ssl.SSLCertVerificationError).

# How to fix SSL Certificate issue on Windows

Firstly, try updating your OS, wouldn't hurt to try.

Now, if you're still having an issue, you would need to download the certificate for the SSL.

The SSL Certificate, Sectigo (cert vendor) provides a download link of an [SSL certificate](https://crt.sh/?id=2835394). You should find it in the bottom left corner, shown below:

A picture where to find the certificate in the website is:
![location of certificate](/static/images/content/fix-ssl-certificate/pem.png)

You have to setup the certificate yourself. To do that you can just click on it, or if that doesn't work, refer to [this link](https://portal.threatpulse.com/docs/sol/Solutions/ManagePolicy/SSL/ssl_chrome_cert_ta.htm)

# How to fix SSL Certificate issue on Mac

Navigate to your `Applications/Python 3.x/` folder and double-click the `Install Certificates.command` to fix this.
