from discord.ext import commands
import discord
import requests
import json

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content.lower()
        if ('covid' in msg) or ('sars-cov-2' in msg):
            url = "https://api.apify.com/v2/key-value-stores/3Po6TV7wTht4vIEid/records/LATEST?disableRedirect=true"

            response = requests.get(url)

            data = response.json()

            covid_data = data

            embedVar = discord.Embed(title="COVID 19 (statystyki)", description="Dane rządowe", color=0xff0f0f)

            embedVar.add_field(name="Zakażono dziś", value=covid_data['dailyInfected'], inline=False)
            embedVar.add_field(name="Przetestowano dziś", value=covid_data['dailyTested'], inline=False)
            embedVar.add_field(name="Zmarło dziś", value=covid_data['dailyDeceased'], inline=False)
            embedVar.add_field(name="Wyzdrowiało dziś", value=covid_data['dailyRecovered'], inline=False)
            embedVar.add_field(name="Zakażono", value=covid_data['infected'], inline=False)
            embedVar.add_field(name="Zmarło", value=covid_data['deceased'], inline=False)
            embedVar.add_field(name="Wyzdrowiało", value=covid_data['recovered'], inline=False)
            embedVar.add_field(name="Wysłano na kwarantanne", value=covid_data['dailyQuarantine'], inline=False)

            embedVar.set_footer(text="Ostatnia aktualizaca danych: " + covid_data['txtDate'])

            await message.channel.send(embed=embedVar)