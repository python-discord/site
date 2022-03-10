---
title: Discord Messages with Colors
description: A guide on how to add colors to your codeblocks on Discord
---

Discord is now slowly rolling out the ability to send colored messages within code blocks. It uses the ANSI color codes, so if you've tried to print colored text in your terminal or console with Python or other languages then it will be easy for you.

To be able to send a colored text, you need to use the `ansi` language for your code block and provide a prefix of this format before writing your text:
```
\u001b[{format};{color}m
```
*The `\u001b` is the unicode for ESCAPE/ESC, see <http://www.unicode-symbol.com/u/001B.html>.* ***If you want to use it yourself without bots, then you need to copy paste the character from the website.***

After you've written this, you can type and text you wish, and if you want to reset the color back to normal, then you need to use `\u001b[0m` as prefix.

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

* 40: Some very dark blue
* 41: Orange
* 42: Gray
* 43: Light gray
* 44: Even lighter gray
* 45: Indigo
* 46: Again some gray
* 47: White

Let's take an example, I want a bold green colored text with the very dark blue background.
I simply use `\u001b[0;40m` (background color) and `\u001b[1;32m` (text color) as prefix. Note that the order is **important**, first you give the background color and then the text color.<br>
Alternatively you can also directly combine them into a single prefix like the following: `\u001b[1;40;32m` and you can also use multiple values. Something like `\u001b[1;40;4;32m` would underline the text, make it bold, make it green and have a dark blue background.

Raw message:<br>
\`\`\`ansi<br>
\u001b[0;40m\u001b[1;32mThat's some cool formatted text right?<br>
or<br>
\u001b[1;40;32mThat's some cool formatted text right?<br>
\`\`\`

Result:<br>
![Background and text color](https://media.discordapp.net/attachments/739937507768270939/930460020603224084/Background-Text-Color.png)

The way the colors look like on Discord is shown in the image below:
![ANSI Colors](https://media.discordapp.net/attachments/739937507768270939/930825555803263016/ANSI-Colors.png)

Note: If the change as not been brought to you yet, or other users, then you can use other code blocks in the meantime to get colored text. See this gist: <https://gist.github.com/matthewzring/9f7bbfd102003963f9be7dbcf7d40e51>
