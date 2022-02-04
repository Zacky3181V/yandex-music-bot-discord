
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



#client = commands.Bot(command_prefix='?', intents = discord.Intents.all())


bot.run(config.TOKEN)