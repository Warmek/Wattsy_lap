import discord
from discord.ext import commands
import os
import requests
import time
import random
import asyncio

from discord.utils import get

class Meme(commands.Cog):
    def __init__(self, client):
        self.admin = 'Dr.Warmek#7292'

        self.client = client




    @commands.command(name="meme", help="Sends memes. You can pass redit and amount (up to 50) as arguments",)
    async def meme(self, ctx, *args):
        if len(args) > 2:
            if int(args[0]) > 50:
                await ctx.send("https://i.ytimg.com/vi/ZEmEtPkd4IQ/hqdefault.jpg")
            else:
                response = requests.get("https://meme-api.herokuapp.com/gimme" + "/" + "/".join(args))
                count = response.json()['count']
                if count < 1:
                    url = response.json()['url']
                    await ctx.send(url)
                else:
                    memes = response.json()['memes']
                    for x in range(count):
                        url = memes[x].get('url')
                        await ctx.send(url)
        else:
            print(args[0])
            if int(args[0]) > 1:
                await ctx.send("https://i.ytimg.com/vi/ZEmEtPkd4IQ/hqdefault.jpg")
            else:
                response = requests.get("https://meme-api.herokuapp.com/gimme" + "/" + "/".join(args))
                count = response.json()['count']
                if count < 1:
                    url = response.json()['url']
                    await ctx.send(url)
                else:
                    memes = response.json()['memes']
                    for x in range(count):
                        url = memes[x].get('url')
                        await ctx.send(url)

    @commands.command(name="say_times", help="Makes bot say things, couple of times", pass_context=True)
    async def say(self, ctx, arg, *args):

        x = int(arg)
        mg = " ".join(args)

        if (str(ctx.message.author) == self.admin):
            await ctx.channel.purge(limit=1)

            if mg == "":
                await ctx.send("Please specify a message to send")
            else:
                for i in range(x):
                    await ctx.send(mg)
                    if(i+1!=x):
                        #ran = random.randint(0, 20) * 30
                        ran = 5
                        print("Delay: " + str(ran) + " secounds")
                        await asyncio.sleep(ran)

        else:
            print(mg)
            file = discord.File("magic.png", filename="magic.png")
            await ctx.send("Where is Lary?", file=file)

    @commands.command(pass_context=True)
    async def addrole(self, ctx, arg):
        member = ctx.message.author
        role = get(ctx.guild.roles, id=int(arg))
        await member.add_roles(role)

    @commands.command()
    async def roles(self, ctx):
        print("\n".join([(str(r.name) + " -> " + str(r.id)) for r in ctx.guild.roles]))

    @commands.command(name="salut", help="", pass_context=True)
    async def mf(self, ctx):
        mf = "....................../´¯/)\n....................,/¯../\n.................../..../\n............./´¯/'...'/´¯¯`·¸\n........../'/.../..../......./¨¯\\\n........('(...´...´.... ¯~/'...')\n.........\.................'...../\n..........''...\.......... _.·´\n............\..............(\n..............\.............\..."
        await ctx.send(mf)

    @commands.command()
    async def emoivb(self, ctx, channel: discord.VoiceChannel, *, new_name):
        print(channel.name + " -> " + new_name)
        await channel.edit(name=new_name)
        print("Done")

    @commands.command()
    async def servers(self, ctx):
        activeservers = self.client.guilds
        if (str(ctx.message.author) == self.admin):
            for guild in activeservers:
                channel = guild.text_channels[0]
                await ctx.send(guild.name)
                link = await channel.create_invite(max_age=300)
                await ctx.send("Here is an instant invite to your server: " + link.url)
