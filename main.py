import config
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get


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

@bot.command()
async def play(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    source = FFmpegPCMAudio('/home/kirill/tools/as.mp3')
    player = voice.play(source)

#client = commands.Bot(command_prefix='?', intents = discord.Intents.all())


bot.run(config.TOKEN)
