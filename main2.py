import discord
from discord.ext import commands
import youtube_dl
import os
import requests
import time
import pafy

from youtube_dl import YoutubeDL






client = commands.Bot(command_prefix="^^")

TOKEN = 'NzE3NzQ1NDExNTk0Mzg3NjI1.XteygQ.ayHQvE7dGBwxYmWJamGX9GlAeXk'

def get_url_form_playlist(yt_url):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'quiet': True, })
    video = ""
    url_list = []

    with ydl:
        result = ydl.extract_info \
            (yt_url, download=False)  # We just want to extract the info

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries']

            # loops entries to grab each video_url
            for i, item in enumerate(video):
                video = result['entries'][i]
                #url_list.append(result['entries'][i]['id'])
                url_list.append(result['entries'][i]['webpage_url'])
                print(result['entries'][i]['webpage_url'])
    return url_list

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------------------")





@client.command()
async def meme(ctx, *args):
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
        print(args[1])
        if int(args[1]) > 50:
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


@client.command(pass_context=True)
async def test(ctx):
    print("test")


@client.command(pass_context=True)
async def play(ctx, url : str):
    await ctx.send("Playing")
    channel = ctx.author.voice.channel.name


    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel)

    await voice_channel.connect()

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    urls = {}
    if "watch" in url:
        urls.append(url)

    else:
        if "playlist" in url:
            print("serching for playlist")
            urls = get_url_form_playlist(url)
        else:
            ctx.send("Use valid url")

    for video in urls:
        print("number: " + video)
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video, download=False)
            video_url = info_dict.get("url", None)
            video_duration = info_dict.get('duration', None)
            video_id = info_dict.get("id", None)
            video_title = info_dict.get('title', None)
        #print(video_url)
        FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        song_one = "ETZwNXk9DeM"

        song = pafy.new(song_one)
        audio = song.getbestaudio()

        print(audio.url)

        voice.play(discord.FFmpegPCMAudio(audio.url, **FFMPEG_OPTS))
        voice.is_playing()
        print(video_duration)
        time.sleep(video_duration)


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


client.run(TOKEN)

# If you wish to securely hide your token, you can do so in a .env file.
# 1. Create a .env in the same directory as your Python scripts
# 2. In the .env file format your variables like this: VARIABLE_NAME=your_token_here
# 3. At the top of the Python script, import os
# 4. In Python, you can read a .env file using this syntax:
# token = os.getenv(VARIABLE_NAME)