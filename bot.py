from discord import client
import requests
import discord
from urlextract import URLExtract
import os
def getVideoLink(url : str) -> str:
    post_url = url
    if (post_url[-1] == '/'):
        post_url = post_url[:-1]
    try:
        video = requests.get(url + ".json", headers = {'User-agent': 'videoGetterBot'}).json()
    except KeyError:
        return
    videoUrl = video[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
    return videoUrl

class RedditVideoBot(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message : discord.Message):
        if (message.author.bot) :
            return
        extractor = URLExtract()
        contentURL = (extractor.find_urls(message.content))
        if (contentURL is not None or "reddit.com" in contentURL[0]):
            videolink = getVideoLink(message.content)
            if (videolink != ""):
                await message.reply(videolink)
                await message.channel.send(message.author.mention)
                await message.delete()
token = os.environ.get('TOKEN')
client = RedditVideoBot()
client.run(token)