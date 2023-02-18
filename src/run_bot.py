import asyncio
import discord
from dotenv import load_dotenv
import os
from discord.ext.commands import Bot
from fastapi import FastAPI
from datetime import timedelta, datetime
from pray import fetch_pray_info, correct_tr, get_pray_info, freetime_info


app = FastAPI()

load_dotenv()
TOKEN = os.environ.get('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = Bot(command_prefix='!', help_command=None, intents=intents)
delta = timedelta(minutes=30)
print(delta)
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
    print(cache)
    # get the message content
    msg = message.content.lower()
    cont = msg.split()
    print(msg)
    print(msg.split())
    # reply to the ping message
    if "/ping" in msg and len(msg) == 5:
        await message.reply(message.author, mention_author=False)

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
                await message.reply(response, mention_author=False)
            except Exception as e:
                await message.reply(e, mention_author=False)
        else:
            await message.reply("Please type city name only, after the command!", mention_author=False)

    if "/vakit" in msg:
        if len(cont) == 2:
            city = correct_tr(cont[1]).lower()
            try:
                response = get_pray_info(fetch_pray_info(city=city))
                await message.reply(response, mention_author=False)
            except Exception as e:
                await message.reply(e, mention_author=False)
        else:
            await message.reply("Please provide city name only, after the command!", mention_author=False)

  
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

