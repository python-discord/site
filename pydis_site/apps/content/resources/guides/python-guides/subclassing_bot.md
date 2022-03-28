---
title: Subclassing Bot
description: "Subclassing the Bot to add more functionality and customisability."
---

## Basic Subclassing
First,  a [basic article](https://www.codesdope.com/course/python-subclass-of-a-class/) on subclassing will provide some fundamental knowledge, which is highly suggested before moving on to this topic, as subclassing [Bot](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot) can ultimately be a complicated task.

## The benefits of subclassing bot
Subclassing Bot can be very beneficial as it provides you with more control and customisability of how your bot functions, also allowing you to add extra features, such as custom bot attributes or methods. For example, the default [Context](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Context) can be overriden to add more functionality.

There are two ways to subclass `commands.Bot`, as shown below:
```py
class CustomBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=#your prefix here as a string
            intents=#your intents here
            #other kwargs can be put here
        )
        # custom bot attributes can be set here, for example:
        self.launch_time = datetime.datetime.utcnow()
        self.example_integer = 5


    async def start(self, *args, **kwargs):
    # here you are overriding the default start method. You can do some code here for example establish a database connection
    # as shown in this example below
    self.db = await aiosqlite.connect('database file name.db')
        await super().start(*args, **kwargs)


bot = CustomBot()
token = YOUR_TOKEN_HERE
bot.run(token)
```
Or
```py
class CustomBot(commands.Bot):
    def __init__(self, *args, **kwargs): # the key-word arguments are not specified here, unlike the example above

        super().__init__(*args, **kwargs)
        # custom bot attributes can be set here, for example:
        self.example_string = 'This is an example!'

    # You can add a custom bot method, anyhting can be done in this function. This is an example:
    def hello(self):
            return 'Hello World'

# Here you set the *args and **kwargs
bot = CustomBot(command_prefix="!", intents=discord.Intents.default())

@bot.command()
async def example(ctx):
    print(bot.hello())
    # In this case, this will print Hello World!
```
With either of the above examples, you are not required to change any of the existing or future code, it is identical to code done without subclassing bot.

To access the custom bot attributes set in the subclass, in the main bot file (in the context of the above example), `bot.variable_name` would be used, and as for cogs, it would be `self.bot.variable_name`. For the custom methods set, in the main file it would be `bot.custom_method()` in the main file and `self.bot.custom_method()` in a cog file.
