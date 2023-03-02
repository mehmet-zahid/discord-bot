
from discord.ext import commands, menus
from discord.ext.commands import Context

from helpers import checks
from mymenu import MyMenu, Confirm, Source



# Here we name the cog and create a new class for the cog.
class Template(commands.Cog, name="template"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="menu",
        description="This is a testing command that does nothing.",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    # This will only allow owners of the bot to execute the command -> config.json
    @checks.is_owner()
    async def menu(self, context: Context):
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        m = MyMenu()
        await m.start(context)

    @commands.hybrid_command(
        name="delete",
        description="This is a testing command that does nothing.",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    # This will only allow owners of the bot to execute the command -> config.json
    @checks.is_owner()
    async def delete_things(self, ctx):
        confirm = await Confirm('Delete everything?').prompt(ctx)
        if confirm:
            await ctx.send('deleted...')


    


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Template(bot))