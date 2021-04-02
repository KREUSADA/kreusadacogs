from redbot.core import Config, commands


class PingInvoke(commands.Cog):
    """
    Bot? [botname]?

    Invoke the ping command by asking if your bot is there.
    """

    __author__ = ["Kreusada", ]
    __version__ = "1.1.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 32482347932, force_registration=True)
        self.config.register_global(botname=None)
    
    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    @commands.group()
    @commands.is_owner()
    async def pingi(self, ctx):
        """Commands to configure PingInvoke."""

    @pingi.command(name="set")
    async def _set(self, ctx, botname: str):
        """
        Set the bot name to listen for.

        Example Input:
        `[p]pingi set wall-e`
        `[p]pingi set r2d2`
        `[p]pingi set [botname]`

        Usage:
        When you type [botname]?, or whatever you configure your name as,
        it will invoke the ping command.
        
        NOTE: Do not include the question mark.
        """
        await self.config.botname.set(botname)
        await ctx.send(f"{ctx.me.name} will now invoke the ping command when it hears `{botname}?`.")

    @pingi.command()
    async def reset(self, ctx):
        """Reset and disable PingInvoke."""
        await ctx.tick()
        await self.config.botname.clear()

    @pingi.command()
    async def settings(self, ctx):
        """Show the current settings for PingInvoke."""
        botname = await self.config.botname()
        if botname:
            await ctx.send(f"{ctx.me.name} will respond to `{botname}?`.")
        else:
            await ctx.send("A name has not been set.")

    @commands.Cog.listener()
    async def on_message_without_command(self, message):
        defa = await self.config.botname()
        if not defa:
            return
        if not message.guild:
            return
        if message.author.bot:
            return
        if message.content.lower().startswith(defa.lower()) and message.content.endswith('?'):
            ctx = await self.bot.get_context(message)
            return await ctx.invoke(self.bot.get_command('ping'))
