---
title: Subclassing Context
description: "Subclassing the default commands.Context to add more functionability and customisability."
---

## Basic Subclassing
First, the [documentation on inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance) on subclassing will provide some fundamental knowledge, which is highly suggested before moving on to this topic, as subclassing [Context](https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Context) can ultimately be a complicated task.

## The benefits of subclassing Context
Subclassing Context can be very beneficial as it allows you to set custom Context methods that can be used in your code. Some applications and examples are provided below.

In order to subclass Context, you are required to subclass `commands.Bot` as well. More on subclassing Bot can be read here [link placeholder] but here is a short example.

```py
# This View is for the prompt function below in the Context subclass.
# This is completely optional and its purpose is demonstrating applications of subclassing Context.


class PromptView(discord.ui.View):
    def __init__(
        self,
        *,
        timeout: float,
        author_id: int,
        ctx: commands.Context,
        delete_after: bool,
    ) -> None:
        super().__init__(timeout=timeout)
        self.value: typing.Optional[bool] = None
        self.delete_after: bool = delete_after
        self.author_id: int = author_id
        self.ctx: Context = ctx
        self.message: typing.Optional[discord.Message] = None
    '''ensure that other members do not confirm or deny'''
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user and interaction.user.id == self.author_id:
            return True
        else:
            await interaction.response.send_message(
                "This confirmation dialog is not for you.", ephemeral=True
            )
            return False

    async def on_timeout(self) -> None:
        if self.delete_after and self.message:
            await self.message.delete()
        # delete the message if there is no response

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.value = True  # returns True if the confirm button is pressed
        await interaction.response.defer()
        if self.delete_after:
            await interaction.delete_original_message()
        self.stop()  # stops the view and deletes the confirmation message

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False  # returns False if the cancel button is pressed
        await interaction.response.defer()
        if self.delete_after:
            await interaction.delete_original_message()
        self.stop()  # stops the view and deletes the confirmation


# We have made two buttons, one for Confirm and one for Cancel.


class CustomContext(commands.Context):
    # create new Context methods here. For example:

    async def send_embed(self, message, **kwargs):
        return await self.send(
            embed=discord.Embed(
                description=message, colour=discord.Color.blurple(), **kwargs
            )
        )
        # This is a shortcut method to sending a custom embed. Pre-set values can be put here, for example the color kwarg in the example above means it has a pre-set color of blurple

    async def send_error_embed(self, message, **kwargs):
        return await self.send(
            embed=discord.Embed(
                description=message, colour=discord.Color.red(), **kwargs
            )
        )
        # embed with pre-set color of red

    async def send_sucess_embed(self, message, **kwargs):
        return await self.send(
            embed=discord.Embed(
                description=message, colour=discord.Color.green(), **kwargs
            )
        )
        # embed with pre-set color of green

    # our custom prompt function using buttons
    async def prompt(
        self,
        message: str,
        *,
        timeout: float = 60.0,
        delete_after: bool = True,
        author_id: Optional[int] = None,
    ) -> Optional[bool]:
        """
        Parameters
        message: str
            The message to show along with the prompt.

        timeout: float (Defaults to 60 seconds)
            How long to wait before stopping the view
        delete_after: bool (Defaults to True)
            Whether to delete the confirmation message after we're done.

        author_id: Optional[int] (Defaults to ctx.author)
            The member who should respond to the prompt.
        -------
        Returns
            True if the confirm button is pressed,
            False if cancel button is pressed,
            None if automatically denied due to no response
        """

        author_id = author_id or self.author.id
        # use the View we have made above and set the arguments
        view = PromptView(
            timeout=timeout,
            delete_after=delete_after,
            ctx=self,
            author_id=author_id,
        )

        view.message = await self.send(message, view=view)
        await view.wait()
        return view.value  # Can return True, False or None


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            # key word arguments
        )

    async def get_context(
        self, message, *, cls=CustomContext
    ):  # When overriding this method, you pass your new Context class to the super() method indicating that there is a new Context class the bot will use.
        return await super().get_context(message, cls=cls)


bot = Bot()

# A command example using subclassed Context:
@bot.command()
async def embed(ctx):
    await ctx.send_embed("This is a subclassed embed!")
    # This would send an embed with the description of the specified string and the embed color wold be Blurple, even though you have not specified it in making the embed, is was set as the pre-set value. You can add more kwargs in sending the embed. For example:

    await ctx.send_success_embed(
        "This is another example of a subclassed embed!",
        title="Subclassing Embed",
        timestamp=datetime.datetime.utcnow(),
    )


# example of the prompt function. It can be used before carrying out big or dangerous operations. For example a massban command where multiple members can be passed in to the member argument
@bot.command()
async def massban(ctx, members: commands.Greedy[discord.Member]):

    request_confirm = await ctx.prompt(f"Are you sure you want to ban {len(members)}?")
    if request_confirm is False:
        # the user cancelled so we can return
    elif request_confirm is True:
        # the user confirmed so we can continue with the command

```
