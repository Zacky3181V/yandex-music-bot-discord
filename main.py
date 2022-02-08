import config
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
import music
import re
from bs4 import BeautifulSoup
import requests
import os
import time

#client = discord.Client(command_prefix = '!')
bot = commands.Bot(command_prefix=config.PREFIX)

@bot.command()
async def hi(ctx):
    author = ctx.message.author
    await ctx.send(f'sup, {author.mention}')
    
@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
        
#накодил zacky
@bot.command()
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.pause()
    
    await ctx.send('Поставили на паузу')

@bot.command()
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.resume() 
    await ctx.send('Возобновили')

@bot.command()
async def play(ctx):
    url = ctx.message.content[6:].format(ctx.message)
    pattern = re.compile("(track)")

    if pattern.search(url):
        if os.path.exists("as"):
            os.remove("as")
            if ctx.message.content.startswith('!play'):
                info = music.infoTrack(url)
                durationTrack = info.get('duration')
                await ctx.send(f"Название трека: {info.get('name')}\nАльбом: {info.get('album')}\nИсполнитель(-ли): {info.get('artists')}\nЖанр: {info.get('genre')}\nДлина трека: {await secondToMinutes(durationTrack)}\nНачинаю скачивать...")
                music.download(url)
                await ctx.send("Включаю песню")
                await playLocalFile(ctx)
        else:
            if ctx.message.content.startswith('!play'):
                info = music.infoTrack(url)
                durationTrack = info.get('duration')
                await ctx.send(f"Название трека: {info.get('name')}\nАльбом: {info.get('album')}\nИсполнитель(-ли): {info.get('artists')}\nЖанр: {info.get('genre')}\nДлина трека: {await secondToMinutes(durationTrack)}\nНачинаю скачивать...")
                music.download(url)
                await ctx.send("Включаю песню")
                await playLocalFile(ctx)
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        quotes = soup.find_all('a', class_='d-track__title deco-link deco-link_stronger')
        for title in quotes:
            s = title.text.strip(), title.get('href')   
            url = "https://music.yandex.ru" + s[1]
            info = music.infoTrack(url)
            durationTrack = info.get('duration')
            await ctx.send(f"Название трека: {info.get('name')}\nАльбом: {info.get('album')}\nИсполнитель(-ли): {info.get('artists')}\nЖанр: {info.get('genre')}\nДлина трека: {await secondToMinutes(durationTrack)}\nНачинаю скачивать...")
            music.download(url)
            await ctx.send("Включаю песню")
            await playLocalFile(ctx)
            time.sleep(int(float(durationTrack)))

async def secondToMinutes(second):
    second = int(float(second))
    h = str(second // 3600)
    m = (second // 60) % 60
    s = second % 60
    if m < 10:
        m = '0' + str(m)
    else:
        m = str(m)
    if s < 10:
        s = '0' +str(s)
    else:
        s = str(s)
    return h + ':' + m + ':' + s

async def playLocalFile(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("Вы не подключены к голосовому чату :(")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    source = FFmpegPCMAudio('as')
    player = voice.play(source)

bot.run(config.TOKEN)