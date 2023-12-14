---
title: Discord Messages with Colors
description: A guide on how to add colors to your codeblocks on Discord
---

Discord is now *slowly rolling out* the ability to send colored messages within code blocks. It uses the ANSI color codes, so if you've tried to print colored text in your terminal or console with Python or other languages then it will be easy for you.

## Quick Explanation
To be able to send a colored text, you need to use the `ansi` language for your code block and provide a prefix of this format before writing your text:
```ansi
\u001b[{format};{color}m
```
*`\u001b` is the unicode escape for ESCAPE/ESC, meant to be used in the source of your bot (see <http://www.unicode-symbol.com/u/001B.html>).* ***If you wish to send colored text without using your bot you need to copy the character from the website.***

After you've written this, you can now type the text you wish to color. If you want to reset the color back to normal, then you need to use the `\u001b[0m` prefix again.

## Formats
Here is the list of values you can use to replace `{format}`:

* 0: Normal
* 1: **Bold**
* 4: <ins>Underline</ins>

## Colors
Here is the list of values you can use to replace `{color}`:

### Text Colors

* 30: Gray
* 31: Red
* 32: Green
* 33: Yellow
* 34: Blue
* 35: Pink
* 36: Cyan
* 37: White

### Background Colors

* 40: Firefly dark blue
* 41: Orange
* 42: Marble blue
* 43: Greyish turquoise
* 44: Gray
* 45: Indigo
* 46: Light gray
* 47: White

## Example

Let's take an example, I want a bold green colored text with the firefly dark blue background.
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

### ANSI Colors Showcase

The way the colors look like on Discord is shown in the image below:

![ANSI Colors](/static/images/content/discord_colored_messages/ansi-colors.png)

*Message sent to get the output of above can be found [here](https://gist.github.com/kkrypt0nn/a02506f3712ff2d1c8ca7c9e0aed7c06#file-ansi-colors-showcase-md).*

#### Disclaimer

***Note**: The change has been brought to all stable desktop clients. Since syntax highlighting on mobile is far behind, ANSI is not supported on mobile as well. Refer to [this gist](https://gist.github.com/matthewzring/9f7bbfd102003963f9be7dbcf7d40e51) for other syntax highlighting methods.*
