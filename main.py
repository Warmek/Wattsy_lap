import discord
from discord.ext import commands

from dotenv import load_dotenv

import os



# invite link: https://discord.com/api/oauth2/authorize?client_id=717745411594387625&permissions=8&scope=bot

# import all of the cogs
from main_cog import General
from image_cog import Image
from music_cog import music_cog
from music_cog_lavalink import Music
from my_bullshit import Meme

from Covid_stats import Events

print("Setting up!")

client = commands.Bot(command_prefix="^^")

try:
    load_dotenv('.env')
    TOKEN = (os.getenv('TOKEN'))
except:
    print("Getting token form repl.it")
    TOKEN = "$TOKEN"

# remove the default help command so that we can write out own
# client.remove_command('help')

# register the class with the bot
client.add_cog(General(client))
client.add_cog(Image(client))
# client.add_cog(music_cog(client))
client.add_cog(Meme(client))

client.add_cog(Music(client))

client.add_cog(Events(client))

# start the bot with our token


client.run(TOKEN)

