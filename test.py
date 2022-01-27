import discord
from discord.ext import commands
import youtube_dl
import os
import requests
import time


from youtube_dl import YoutubeDL

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

get_url_form_playlist("https://www.youtube.com/playlist?list=PLZD-LZoLyz8IwTNGlfEzC2ai7rHTNJ3vZ")