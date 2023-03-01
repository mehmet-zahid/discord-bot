import asyncio
import discord
from discord import Embed
from dotenv import load_dotenv
import os
from discord.ext import commands
from fastapi import FastAPI
from datetime import timedelta, datetime
from pray import fetch_pray_info, correct_tr, get_pray_info, freetime_info

prefix = '/' 
HELP = [
    {
    "command": "help",
    "parameters": [],
    "usage": prefix + "help",
    "example": prefix + "help"
    },
    {
    "command": "freetime",
    "parameters": ["city_name: str","time_after: int", "duration: float: 1.30 --> hour =1, minutes=30"],
    "usage": prefix + "freetime <city_name> <time_after> <duration>",
    "example": prefix + "freetime istanbul 2 1.30"
    },
    {
    "command": "namaz",
    "parameters": [],
    "usage": prefix + "namaz",
    "example": prefix + "namaz"
    },
    {
    "command": "vakit",
    "parameters": [],
    "usage": prefix + "vakit",
    "example": prefix + "vakit"
    },
    ]

app = FastAPI()
load_dotenv()
TOKEN = os.environ.get('DISCORD_TOKEN')
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)
delta = timedelta(hours=1)
cache = {}


async def send_hello_msg(cache: dict, message, delta: timedelta, hello_msg: str):
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
            cache[message.author.name]["date_last_message"] = message.created_at
    else:
        await message.reply(hello_msg, mention_author=False)
        cache[message.author.name]["date_last_message"] = message.created_at

@bot.command()
async def test(ctx):
    response = 'This text has some words *emphasized* in _different_ ways'
    await ctx.send(response)

@bot.event
async def on_message(message):
    global cache
    msg: str = message.content.lower()
    cont = msg.split()
    #doc = {"Author": message.author.name,
    #       "Message": msg,
    #       "CreatedTime": message.created_at}

    #result = await collection.insert_one(doc)
    #print('result %s' % repr(result.inserted_id))
    
    # Do not reply to self
    #print(message.author.name)
    #print(message.guild)

    if message.author == bot.user:
        return

    # Do not reply to any other bot    
    if message.author.bot:
        return
       
    if message.author.name == "by.NeOn-B1-66-er":
        await send_hello_msg(cache=cache, message=message, delta=delta, hello_msg="Hoşgeldiniz Ahmet Bey, sohbetin tadını çıkarın efendim.")
    if message.author.name == "Muhammed_Samil_Albayrak":
        await send_hello_msg(cache=cache, message=message, delta=delta, hello_msg="Şamil Bey Hoşgeldiniz")
    if message.author.name == "mutex":
        await send_hello_msg(cache=cache, message=message, delta=delta, hello_msg="Hoşgeldiniz Mutex")
    if message.author.name == "Mehmet Zahid IŞIK":
        #await message.author.send("Merhaba, bu bir dm mesajı ve botunuz tarafından gönderildi efendim.")
        await send_hello_msg(cache=cache, message=message, delta=delta, hello_msg="Hello Mehmet Zahid")
        #await message.delete(delay=3.2)
    if message.author.name == "süleyman mercan":
        await send_hello_msg(cache=cache, message=message, delta=delta, hello_msg="Hoşgeldiniz Beyefendi")

    if msg.startswith(prefix):
        command = msg[len(prefix):]
    if "/ping" in msg and len(msg) == 5:
        await message.reply(message.author, mention_author=True)

    if "/ask" in msg:
        await message.reply("this will be implemented...", mention_author=False)

    if "/freetime" in msg:
        if len(cont) == 4:
            city = correct_tr(cont[1]).lower()
            try:
                time_after = int(cont[2])
                if time_after > 10:
                    await message.reply(f"{time_after} is too long time_after value! ", mention_author=False)
                    return
            except Exception as e:
                print(e)
                await message.reply("'time_after' must be like int type! ", mention_author=False)
                return
            try:
                duration = float(cont[3])
                duration = str(duration).split('.')
                hour = int(duration[0])
                min = int(duration[1]) if duration[1] else 0 
                if hour > 5 or min > 59:
                    await message.reply("wrong value for hour(must be 0-6) or minute(must be 0-60) ! ",
                                        mention_author=False)
                    return
            except Exception as e:
                print(e)
                await message.reply("'duration parameter must be like a float type! ", mention_author=False)
                return
            try:
                res = freetime_info(city, time_after, duration=(hour, min))
            except Exception as e:
                print(e)
                return
            await message.reply(res,mention_author=False)

    
    if "/namaz" in msg:
        if len(cont) == 2:
            city = correct_tr(cont[1]).lower()
            print(city)
            try:
                response = fetch_pray_info(city=city)
                embed = Embed.from_dict(response)
                await message.channel.send(embed=embed)
                #await message.reply(response, mention_author=False)
            except Exception as e:
                await message.reply(e, mention_author=False)
        else:
            await message.reply("Please type city name only, after the command!", mention_author=False)

    if "/vakit" in msg:
        if len(cont) == 2:
            city = correct_tr(cont[1]).lower()
            try:
                response = get_pray_info(fetch_pray_info(city=city), as_str=True)
                await message.reply(response, mention_author=False)
            except Exception as e:
                await message.reply(e, mention_author=False)
        else:
            await message.reply("Please provide city name only, after the command!", mention_author=False)



@bot.event
async def on_member_join(member):
    await message.reply(f"Hoşgeldin {member.name}")


    
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

