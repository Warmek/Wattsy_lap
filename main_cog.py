import discord
from discord.ext import commands
import asyncio


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.admin = 'Dr.Warmek#7292'
        self.game_message = "PARTY!!! *spins*"
        self.help_message = """
```
General commands:
/help - displays all the available commands
/clear amount - will delete the past messages with the amount specified

Image commands:
/search <keywords> - will change the search to the keyword
/get - will get the image based on the current search

Music commands:
/p <keywords> - finds the song on youtube and plays it in your current channel
/q - displays the current music queue
/skip - skips the current song being played
```
"""
        self.text_channel_list = []

    #some debug info so that we know the bot has started    
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel)

        #await self.send_to_all(self.help_message)

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Pornhub Kids"))
        #await self.bot.change_presence(activity=discord.Streaming(name="Pornhub Kids", url="google.com"))

        #print(self.bot.user.id)
        print("Bot ready")

    """
        @commands.command(name="help", help="Displays all the available commands")
        async def help(self, ctx):
            await ctx.send(self.help_message)

        async def send_to_all(self, msg):
            for text_channel in self.text_channel_list:
                await text_channel.send(msg)
    """

    @commands.command(name="invite", help="Generates invite link")
    async def invite_link(self, ctx):
        await ctx.send("https://discord.com/api/oauth2/authorize?client_id=717745411594387625&permissions=8&scope=bot")

    @commands.command(name="say", help="Makes bot say things", pass_context=True)
    async def say(self, ctx, *args):

        mg = " ".join(args)

        if (str(ctx.message.author) == self.admin):
            try:
                await ctx.channel.purge(limit=1)
            except:
                print("No perrmision to delete messages")

            if mg == "":
                await ctx.send("Please specify a message to send")
            else:
                await ctx.send(mg)
        else:
            print(mg)
            file = discord.File("magic.png", filename="magic.png")
            await ctx.send("Where is Lary?", file=file)

    @commands.command(name="Kill_him", pass_context=True)
    async def kh(self, ctx, number : int):
        if (str(ctx.message.author) == self.admin):
            await ctx.channel.purge(limit=number+1)
        else:
            file = discord.File("magic.png", filename="magic.png")
            await ctx.send("Where is Lary?", file=file)


    @commands.command(name="clean_up", help="Clears a specified amount of messages")
    async def clean_up(self, ctx, arg : int):
        if (str(ctx.message.author) == self.admin):
            arg = arg + 1
            await ctx.channel.purge(limit=arg)
        else:
            file = discord.File("magic.png", filename="magic.png")
            await ctx.send("Where is Lary?", file=file)

    @commands.command(name="only_pic", aliases=['op'], help="Clears chanel from non pictures")
    async def clear_pic(self, ctx):
        await ctx.message.delete()
        mgs = []
        i = 0
        async for x in ctx.message.channel.history():
            i+=1
            if not x.attachments:
                await x.delete()
                await asyncio.sleep(0.6)
            print(i)
        print("done")
