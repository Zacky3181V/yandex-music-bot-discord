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

activity = discord.Activity(type=discord.ActivityType.watching, name="!helpBot")
bot = commands.Bot(command_prefix=config.PREFIX, activity=activity, status=discord.Status.idle)

@bot.command()
async def hi(ctx):
    author = ctx.message.author
    await ctx.send(f'sup, {author.mention}')

@bot.command()
async def helpBot(ctx):
    await ctx.send(f'[--------------------------------Команды---------------------------------]\n*!play* <ссылкаНаТрекИлиАльбом> - воспроизведение песни или альбома **ВНИМАНИЕ:** Исполнитель команды должен находится в VoiceChannel\n*!stop* - Бот выйдет из VoiceChanell, музыка прервётся\n*!pause* - Можно не объяснять :)\n*!resume* - Тоже можно не объяснять :)\n[-------------------------Информация о боте---------------------------]\nРазработчики: KirMozor#6756 и delay120#2363\nGitHub: https://github.com/Zacky3181V/yandex-music-bot-discord\nПожелания и отчёты о багах писать в GitHub\n**Псс...** донатики тоже на странице GitHub скидывайте')
    
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
async def next(ctx):
    if len(queue)>1:
        voice_channel = ctx.voice_client
        voice_channel.stop()
        queue.pop(0)
        info = music.infoTrack(queue[0])
        await ctx.send(f"Название трека: {info.get('name')}\nАльбом: {info.get('album')}\nИсполнитель(-ли): {info.get('artists')}\nЖанр: {info.get('genre')}\nДлина трека: {await secondToMinutes(info.get('duration'))}\nНачинаю скачивать...")
        music.download(queue[0])
        await playLocalFile(ctx, int(float(info.get('duration'))))
    else:
        #ctx.send('**Нет треков в очереди**')
        pass

@bot.command()
async def clean(ctx):
    if len(queue)==1:
        await ctx.send('**Нет треков в очереди, очищать нечего**')
    else:
        for tracks in reversed(range(1,len(queue))):
            queue.pop(tracks)
        await ctx.send('**Очередь очищена, добавляй следующие треки**')

@bot.command()
async def add(ctx):
    added_track_url = ctx.message.content[4:].format(ctx.message)
    queue.append(added_track_url)
    await ctx.send('**Добавлен новый трек в очередь**')

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
async def play(ctx):
    url = ctx.message.content[6:].format(ctx.message)
    pattern = re.compile("(track)")

    if pattern.search(url):
            if ctx.message.content.startswith('!play'):
                info = music.infoTrack(url)
                durationTrack = info.get('duration')
                await ctx.send(f"Название трека: {info.get('name')}\nАльбом: {info.get('album')}\nИсполнитель(-ли): {info.get('artists')}\nЖанр: {info.get('genre')}\nДлина трека: {await secondToMinutes(durationTrack)}")
                await playLocalFile(ctx, int(float(durationTrack)), url)
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        quotes = soup.find_all('a', class_='d-track__title deco-link deco-link_stronger')
        global queue
        queue = []
        for title in quotes:
            s = title.text.strip(), title.get('href')   
            url = "https://music.yandex.ru" + s[1]
            info = music.infoTrack(url)
            queue.append(url)

            durationTrack = info.get('duration')
            await ctx.send(f"Название трека: {info.get('name')}\nАльбом: {info.get('album')}\nИсполнитель(-ли): {info.get('artists')}\nЖанр: {info.get('genre')}\nДлина трека: {await secondToMinutes(durationTrack)}")
            await playLocalFile(ctx, int(float(durationTrack)), url)

@bot.command()
async def playLocalFile(ctx, second, url):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("Вы не подключены к голосовому чату :(")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    url_parts=url.split('/')
    trackID = url_parts[-1]

    url = music.extractDirectLinkToTrack(trackID)
    source = FFmpegPCMAudio(url)
    player = voice.play(source)
    await asyncio.sleep(second)

bot.run(config.TOKEN)
