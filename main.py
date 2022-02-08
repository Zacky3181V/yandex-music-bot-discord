import config
import asyncio
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
    
#удалено join

@bot.command()
async def stop(ctx):
    await ctx.voice_client.disconnect()
        
#накодил zacky
@bot.command()
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = ctx.voice_client #изменил, если обратно вернуть то вместо ctx поставить server
    if voice_channel.is_playing():
        voice_channel.pause()
        await ctx.send('**Поставили на паузу**')
    else:
        if voice_channel.is_paused() == True:
            await ctx.send('**Уже поставлено на паузу**')
        else: 
            await ctx.send('**Упс...похоже, нет проигрываемой музыки**')


@bot.command()
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = ctx.voice_client #изменил, если обратно вернуть то вместо ctx поставить server
    if ctx.voice_client.is_paused() == True:
        voice_channel.resume() 
        await ctx.send('**Возобновили**')
    else:
        await ctx.send('**Вы и не ставили на паузу**')

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
                await playLocalFile(ctx, int(float(durationTrack)))
        else:
            if ctx.message.content.startswith('!play'):
                info = music.infoTrack(url)
                durationTrack = info.get('duration')
                await ctx.send(f"Название трека: {info.get('name')}\nАльбом: {info.get('album')}\nИсполнитель(-ли): {info.get('artists')}\nЖанр: {info.get('genre')}\nДлина трека: {await secondToMinutes(durationTrack)}\nНачинаю скачивать...")
                music.download(url)
                await ctx.send("Включаю песню")
                await playLocalFile(ctx, int(float(durationTrack)))
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
            await playLocalFile(ctx, int(float(durationTrack)))

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

@bot.command()
async def playLocalFile(ctx, second):
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
    await asyncio.sleep(second)

bot.run(config.TOKEN)
