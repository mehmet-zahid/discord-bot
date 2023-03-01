
import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
from pray import fetch_pray_info, set_global_view, BISMILLAH


# Here we name the cog and create a new class for the cog.
class Pray(commands.Cog, name="namaz"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="namaz",
        description="Fetches and shows pray time information.",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def namaz(self, context: Context, city: str):
        """
        Shows current pray information.

        :param context: The application command context.
        """
        pray_info = fetch_pray_info(city)
        embed = discord.Embed(
            title=f'{BISMILLAH}\n**Namaz Vakitleri**',
            description='*Bugün için namaz vakitleri*',
            color=discord.Colour.dark_orange()
        )
        embed.set_footer(text=pray_info['today']['date'])
        for k, v in set_global_view(pray_info['today']['prays']).items():
            embed.add_field(name=k, value=f"```{v}```", inline=False)

        await context.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Pray(bot))