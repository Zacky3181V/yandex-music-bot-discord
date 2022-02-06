
import config

import discord

from discord.ext import commands

import yandex_music

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

@bot.command()
async def whoa(ctx):
    if ctx.message.content.startswith('!whoa'):
        channel = ctx.message.channel
        await ctx.channel.send(ctx.message.content[5:].format(ctx.message))


#client = commands.Bot(command_prefix='?', intents = discord.Intents.all())


bot.run(config.TOKEN)
