
from discord.ext import tasks
from discord.ext.commands import Bot
import discord
import datetime
from zoneinfo import ZoneInfo
from helpers import db_manager
import random
import locale

locale.setlocale(locale.LC_ALL, 'tr_TR')

zone = ZoneInfo("Turkey")
# Here we name the cog and create a new class for the cog.
class Reminder:
    TIMES = [datetime.time(hour=9, minute=30, tzinfo=zone),
             datetime.time(hour=11, tzinfo=zone)]
    LESSON_TIME = datetime.time(hour=12, minute=0, tzinfo=zone)

    def __init__(self, bot: Bot):
        self.bot = bot
        self.remind_lesson.start()
        self.status_task.start()
        self.sunday.start()
        

    def get_sunday_dt(self, tm: datetime.time=None):
        today = datetime.date.today()
        sunday = today + datetime.timedelta(days=(6-today.weekday()))
        if tm is None:
            return sunday

        return datetime.datetime.combine(sunday, tm)
        

    @tasks.loop(time=TIMES)
    async def sunday(self):
        now = datetime.datetime.now(tz=zone)
        
        if self.get_sunday_dt(Reminder.TIMES[0]) <= now >= self.get_sunday_dt(Reminder.TIMES[1]):
            user_ids = await db_manager.get_notifiers()
            async for uid in user_ids:
                user = self.bot.get_user(int(uid[0]))
                
                embed = discord.Embed(
                title="*Hatırlatma Mesajı*",
                description=f"{user.mention} ,\n```Bugün Saat 12.00 için planlanmış olan C++ dersini hatırlatırım, Saygılarımla.```",
                color=0x9C84EF
                )
                await user.send(embed=embed)

    @tasks.loop(hours=24) 
    async def remind_lesson(self) -> None:

        try:
            user_ids = await db_manager.get_notifiers()
            formatted_date = discord.utils.format_dt(self.get_sunday_dt(Reminder.LESSON_TIME), style='D')
            for uid in user_ids:
                user = self.bot.get_user(int(uid[0]))
                embed = discord.Embed(
                    title="*Hatırlatma Mesajı*",
                    description=f"{user.mention} ,\n{formatted_date} Pazar günü saat 12.00 için planlanmış olan C++ dersini hatırlatırım, Saygılarımla.",
                    color=0x9C84EF
                    )
                await user.send(embed=embed)
        except Exception as e:
            print(e)

    @tasks.loop(minutes=5.0)
    async def status_task(self) -> None:
        """
        Setup the game status task of the bot.
        """
        statuses = ["with good me!", "with Mutex!", "with Şamil!", "with Suleyman"]
        await self.bot.change_presence(activity=discord.Game(random.choice(statuses)))   