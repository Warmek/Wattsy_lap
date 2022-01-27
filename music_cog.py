import discord
from discord.ext import commands
import random

from youtube_dl import YoutubeDL
import youtube_dl

class music_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.music_queue = []
        #
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'quiet': True}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}


        self.vc = ""


    def url_to_source(self, video):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            info_dict = ydl.extract_info(video, download=False)
            video_url = info_dict.get("url", None)
            video_id = info_dict.get("id", None)
            video_title = info_dict.get('title', None)
        return video_url

    def get_url_form_playlist(self, yt_url, voice_channel):
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'quiet': True, })
        video = ""
        print(voice_channel)
        with ydl:
            result = ydl.extract_info \
                (yt_url,
                 download=False)  # We just want to extract the info

            if 'entries' in result:
                # Can be a playlist or a list of videos
                video = result['entries']

                # loops entries to grab each video_url
                for i, item in enumerate(video):
                    video = result['entries'][i]
                    video_url = self.url_to_source(result['entries'][i]['webpage_url'])
                    video_title = result['entries'][i]['title']
                    song = {'source': video_url, 'title': video_title}
                    print(video_title + " -> Downloaded")
                    self.music_queue.append([song, voice_channel])

        print("Playlist downloaded")

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']
            title = self.music_queue[0][0]['title']


            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            title = self.music_queue[0][0]['title']
            
            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])


            """
            #print("Is connected: " + self.vc.is_connected())

            if ():
                await ctx.author.voice.channel.connect()

            #-------------
            """
            """
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
                print("connecting")
            else:
                await self.vc.move_to(self.music_queue[0][1])

            #print(self.music_queue)
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)
            """

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def p(self, ctx, *args):
        query = "".join(args)
        
        voice_channel = ctx.author.voice.channel



        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        else:
            if "playlist" in query:
                print("playing playlist")
                await ctx.send("I got u fam")
                self.get_url_form_playlist(query, voice_channel)
            else:
                song = self.search_yt(query)
                if type(song) == type(True):
                    await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
                else:
                    await ctx.send("Song added to the queue")
                    self.music_queue.append([song, voice_channel])

            if self.is_playing == False:
                print("Joinnig: " + self.music_queue[0][1].name)
                await ctx.send("Joinnig: " + self.music_queue[0][1].name)
                await self.play_music()

    @commands.command(name="queue", help="Displays the current songs in queue")
    async def q(self, ctx):
        retval = ""
        v = 0
        for i in range(0, len(self.music_queue)):
            retval += str(i+1) + " : " + self.music_queue[i][0]['title'] + "\n"
            if(i>=24):
                break

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="join", help="Wattsy joins you :)")
    async def jo(self, ctx):
        await ctx.author.voice.channel.connect()


    @commands.command(name="leave", help="Wattsy leaves you :(")
    async def le(self, ctx):
        server = ctx.message.guild.voice_client
        await server.disconnect()

    @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx, *args):

        if len(args) == 0:
            args[0]==1
        for i in args[0]:
            if self.vc != "" and self.vc:
                self.vc.stop()
                #try to play next in the queue if it exists
                await self.play_music()

    @commands.command(name="shuffle", help="Shuffles the queue... DUH")
    async def shuffle(self, ctx):
        random.shuffle(self.music_queue)
        await ctx.send("Shuffled")

    @commands.command(name="clear", help="Clears queue")
    async def clear(self, ctx):
        self.music_queue.clear()

    @commands.command(name="pause", help="Pauses currently playing song")
    async def pause(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.pause()

    @commands.command(name="resume", help="Resumes playing")
    async def resume(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.resume()

    @commands.command(name="stop", help="Clears queue and stops playing")
    async def stop(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        self.music_queue.clear()
        voice_channel.stop()

    @commands.command(name="remove", help="Removes song by it's id (from queue)")
    async def remove(self, ctx, id : int):
        del self.music_queue[id]

    @commands.command(name="skip_to", help="Puts element on top of queue")
    async def skip_to(self, ctx, *args):
        title = " ".join(args)
        print(self.music_queue[1]['title'])
        self.music_queue.insert(0, self.music_queue.pop(self.music_queue.index(title)))

        self.play_next()