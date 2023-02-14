import asyncio
import discord
from dotenv import load_dotenv
import os
from discord.ext.commands import Bot
from fastapi import FastAPI
import datetime
app = FastAPI()

load_dotenv()
TOKEN = os.environ.get('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = Bot(command_prefix='!', help_command=None, intents=intents)
delta = datetime.timedelta(minutes=30)
print(delta)
cache = {}

async def send_hello_msg(cache: dict, message, delta: datetime.timedelta, hello_msg: str):
    try:
        member_name = cache[message.author.name]
    except KeyError:
        cache[message.author.name] = {"date_last_message":None}
    date_last_message = cache[message.author.name]["date_last_message"]
    if date_last_message:
        fark = message.created_at - date_last_message
        print(fark)
        if fark > delta:
            await message.reply(hello_msg, mention_author=False)
    else:
        await message.reply(hello_msg, mention_author=False)
        cache[message.author.name]["date_last_message"] = message.created_at


@bot.event
async def on_message(message):
    global date_last_message
    global cache
    print(message.author.name)
    print(message.created_at, type(message.created_at))
    # Do not reply to self
    if message.author == bot.user:
        return
    # Do not reply to any other bot
    if message.author.bot:
        return 
    if message.author.name == "Muhammed_Samil_Albayrak":
        await send_hello_msg(cache=cache, message=message, delta=delta, hello_msg="Agam Hoşgeldin :)")
    if message.author.name == "mutex":
        await send_hello_msg(cache=cache, message=message, delta=delta, hello_msg="Paşam seni burda görmek ne güzel :)")
    if message.author.name == "Zahid_Unity1":
        await send_hello_msg(cache=cache, message=message, delta=delta, hello_msg="Agam beni geliştirmeyi ihmal etme :)")
    if message.author.name == "süleyman mercan":
        await send_hello_msg(cache=cache, message=message, delta=delta, hello_msg="Süleyman aga botunu geliştirmeye devam ediyor musun :)")
    # get the message content
    msg = message.content.lower()
    # reply to the ping message
    if "!ping" in msg:
        await message.reply(message.author, mention_author=False)

    if "/ask" in msg:
        await message.reply("this will be implemented...", mention_author=False)
    

@app.get("/")
def main():
    return "The bot is alive!"

# run the bot as a FastAPI async function
@app.on_event("startup")
async def run():
    """
    to run the bot as a FastAPI async func
    """
    try:
        asyncio.create_task(bot.start(TOKEN))
    except:
        await bot.logout()

