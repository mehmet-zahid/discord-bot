
import discord
from discord.ext import commands, menus
from discord.ext.commands import Context
import openai
import os
from helpers import checks
from mymenu import Source

openai.api_key = os.environ.get('OPENAI_API_KEY')

def split_answer(string):
    for i in range(0, len(string), 1000):
        yield string[i:i+1000]

# Here we name the cog and create a new class for the cog.
class Openai(commands.Cog, name="openai"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="gpt",
        description="To talk to Chatgpt from Openai.",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    # This will only allow owners of the bot to execute the command -> config.json
    async def gpt(self, context: Context, prompt: str):
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response['choices'][0]['message']['content']
        embed = discord.Embed(
            title='**ChatGpt **',
            description='**NO CONTEXT!** One time asking! *.\n*Answer:*',
            color=discord.Colour.green()
        )
        answer_length = len(answer)
        print(answer_length)
        for i in split_answer(answer):
            print(len(i))
            embed.add_field(name='ChatGpt:', value=f"```{i}```", inline=False)
        
        #pages = menus.MenuPages(source=MySource(range(1, 100)), clear_reactions_after=True)
        #pages = menus.MenuPages(source=Source(answer, key=lambda t: t.key, per_page=12), clear_reactions_after=True)
        #await pages.start(context)
        await context.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Openai(bot))