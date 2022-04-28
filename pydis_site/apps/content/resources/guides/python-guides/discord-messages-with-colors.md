---
title: Discord Messages with Colors
description: A guide on how to add colors to your codeblocks on Discord
---

Discord is now slowly rolling out the ability to send colored text within code blocks. This is done using ANSI color codes which is also how you print colored text in your terminal.

To send colored text in a code block you need to first specify the `ansi` language and use the prefixes similar to the one below:
```ansi
\u001b[{format};{color}m
```
*`\u001b` is the unicode escape for ESCAPE/ESC, meant to be used in the source of your bot (see <http://www.unicode-symbol.com/u/001B.html>).* ***If you wish to send colored text without using your bot you need to copy the character from the website.***

After you've written this, you can now type the text you wish to color. If you want to reset the color back to normal, then you need to use the `\u001b[0m` prefix again.

Here is the list of values you can use to replace `{format}`:

* 0: Normal
* 1: **Bold**
* 4: <ins>Underline</ins>

Here is the list of values you can use to replace `{color}`:

*The following values will change the **text** color.*

* 30: Gray
* 31: Red
* 32: Green
* 33: Yellow
* 34: Blue
* 35: Pink
* 36: Cyan
* 37: White

*The following values will change the **text background** color.*

* 40: Firefly dark blue
* 41: Orange
* 42: Marble blue
* 43: Greyish turquoise
* 44: Gray
* 45: Indigo
* 46: Light gray
* 47: White

Let's take an example, I want a bold green colored text with the very dark blue background.
I simply use `\u001b[0;40m` (background color) and `\u001b[1;32m` (text color) as prefix. Note that the order is **important**, first you give the background color and then the text color.

Alternatively you can also directly combine them into a single prefix like the following: `\u001b[1;40;32m` and you can also use multiple values. Something like `\u001b[1;40;4;32m` would underline the text, make it bold, make it green and have a dark blue background.

Raw message:
````nohighlight
```ansi
\u001b[0;40m\u001b[1;32mThat's some cool formatted text right?
or
\u001b[1;40;32mThat's some cool formatted text right?
```
````

Result:

![Background and text color result](/static/images/content/discord_colored_messages/result.png)

The way the colors look like on Discord is shown in the image below:

![ANSI Colors](/static/images/content/discord_colored_messages/ansi-colors.png)

Note: If the change as not been brought to you yet, or other users, then you can use other code blocks in the meantime to get colored text. See **[this gist](https://gist.github.com/matthewzring/9f7bbfd102003963f9be7dbcf7d40e51)**.
