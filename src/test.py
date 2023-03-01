from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
from pray import fetch_pray_info, set_global_view, BISMILLAH

load_dotenv()
TOKEN = os.environ.get('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())


@bot.command()
async def namaz(ctx, city):
    print(ctx.author.id)
    
    pray_info = fetch_pray_info(city)
    embed = discord.Embed(
        title=f'Namaz Vakitleri\n{BISMILLAH}',
        description='Bugün için namaz vakitleri',
        color=discord.Colour.dark_orange()
    )
    embed.set_footer(text=pray_info['today']['date'])
    for k, v in set_global_view(pray_info['today']['prays']).items():
        embed.add_field(name=k, value=f"```{v}```", inline=False)

    
    await ctx.send(embed=embed)


bot.run(TOKEN)