import random

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


class Choice(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Heads", style=discord.ButtonStyle.blurple)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.value = "heads"
        self.stop()

    @discord.ui.button(label="Tails", style=discord.ButtonStyle.blurple)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "tails"
        self.stop()

class RockPaperScissors(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Scissors", description="You choose scissors.", emoji="✂"
            ),
            discord.SelectOption(
                label="Rock", description="You choose rock.", emoji="🪨"
            ),
            discord.SelectOption(
                label="paper", description="You choose paper.", emoji="🧻"
            ),
        ]
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = discord.Embed(color=0x9C84EF)
        result_embed.set_author(
            name=interaction.user.name, icon_url=interaction.user.avatar.url
        )

        if user_choice_index == bot_choice_index:
            result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xF59E42
        elif user_choice_index == 0 and bot_choice_index == 2:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 1 and bot_choice_index == 0:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 2 and bot_choice_index == 1:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        else:
            result_embed.description = (
                f"**I won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            )
            result_embed.colour = 0xE02B2B
        await interaction.response.edit_message(
            embed=result_embed, content=None, view=None
        )


class RockPaperScissorsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RockPaperScissors())


class Fun(commands.Cog, name="fun"):
    FACTS = ["İnsan bir yolcudur. Sabavetten gençliğe, gençlikten ihtiyarlığa, ihtiyarlıktan kabre, kabirden haşre, haşirden ebede kadar yolcuğu devam eder.",
             "Bizler uzun bir seferdeyiz. Buradan kabre, kabirden haşre, haşirden ebed memleketine gitmek üzereyiz.",
             "Sen burada misafirsin. Ve buradan da diğer bir yere gideceksin. Misafir olan kimse, beraberce getiremediği bir şeye kalbini bağlamaz.",
             "Bir şeyin şerefi neslinde değildir, zâtındadır. Birşeyin aslını gösteren semeresidir.",
             "Kıymet ve ehemmiyet, kemiyette ve adet çokluğunda değildir.",
             "Paslanmış bîhemta bir elmas, dâima mücella cama müreccahtır.",
             "Birinin âsârı muhakeme olunursa, onun hâssasını nazara almak lazımdır.",
             "Âlâ bir şey bozulsa, ednâ birşeyin bozulmasından daha bozuk olur.\
             \nMesela süt ve yoğurt bozulsalar yine yenilebilir. Yağ bozulsa yenilmez, bazan zehir gibi olur. \
             \nÖyle de mahlukâtın en mükerremi, belki en âlâsı olan insan, eğer bozulsa, bozuk hayvandan daha ziyade bozuk olur.",
             "İnsan, santral gibi, bütün hilkatın nizamlarına ve fıtratın kânunlarına ve kâinattaki nevâmis-i ilâhiyenin şualarına bir merkezdir.",
             "Fıtrat ve vicdan akla bir penceredir. Tevhidin şuâını neşrederler.",
             "Mesmûat, mubsırat, me'kulât âlemlerini ihata eden insandaki duygular, Sâniin sıfat-ı mutlakasını ve geniş şuûnatını fehmetmek içindir."]
    def __init__(self, bot):
        self.bot = bot
        self.rfb = ""

    @commands.hybrid_command(name="fact", description="Get a random fact.")
    @checks.not_blacklisted()
    async def fact(self, context: Context) -> None:
        """
        Get a random fact.
        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        #async with aiohttp.ClientSession() as session:
        #    async with session.get(
        #        "https://uselessfacts.jsph.pl/random.json?language=en"
        #    ) as request:
        #        if request.status == 200:
        #            data = await request.json()
        #            embed = discord.Embed(description=data["text"], color=0xD75BF4)
        #        else:
        #            embed = discord.Embed(
        #                title="Error!",
        #                description="There is something wrong with the API, please try again later",
        #                color=0xE02B2B,
        #            )
        
        rfc = random.choice(Fun.FACTS)
        while self.rfb == rfc:
            rfc = random.choice(Fun.FACTS)
        random_fact = "```" + rfc + "```"
        embed = discord.Embed(
            title= "**Really Excellent Facts**", 
            description=random_fact, 
            color=0xD75BF4)
        await context.send(embed=embed)
        self.rfb = rfc

    @commands.hybrid_command(
        name="coinflip", description="Make a coin flip, but give your bet before."
    )
    @checks.not_blacklisted()
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip, but give your bet before.
        :param context: The hybrid command context.
        """
        buttons = Choice()
        embed = discord.Embed(description="What is your bet?", color=0x9C84EF)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["heads", "tails"])
        if buttons.value == result:
            embed = discord.Embed(
                description=f"Correct! You guessed `{buttons.value}` and I flipped the coin to `{result}`.",
                color=0x9C84EF,
            )
        else:
            embed = discord.Embed(
                description=f"Woops! You guessed `{buttons.value}` and I flipped the coin to `{result}`, better luck next time!",
                color=0xE02B2B,
            )
        await message.edit(embed=embed, view=None, content=None)

    @commands.hybrid_command(
        name="rps", description="Play the rock paper scissors game against the bot."
    )
    @checks.not_blacklisted()
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.
        :param context: The hybrid command context.
        """
        view = RockPaperScissorsView()
        await context.send("Please make your choice", view=view)


async def setup(bot):
    await bot.add_cog(Fun(bot))