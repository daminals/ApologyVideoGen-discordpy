# bot.py
# Handles discord bot functionality
# Daniel Kogan, 06/01/2020

# TODO: create working ci/cd pipeline to push changes to server

import os, sys
import discord, random, asyncio #now using pycord because discordpy no longer maintained
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
TOKEN = os.environ.get('TOKEN', 3)

bot = commands.Bot(command_prefix='s!', intents=intents) # until pycord updates
# TODO: add voice only support for VC

from sorry_engine import *

bot.remove_command('help')

async def updown(message):
    await message.add_reaction('<:upvote:776161705960931399>')
    await message.add_reaction('<:downvote:776162465842200617>')

@bot.event
async def on_ready():
    await bot.tree.sync()
    servers = list(bot.guilds)
    server_num = len(servers)
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {server_num} servers| s!help"))
    print('bot.py is active')

@bot.event
async def on_command(ctx):
  if not (ctx.interaction):
    await ctx.message.add_reaction('✅')

@bot.hybrid_command(name='sorry')
async def sorry(ctx, *, reason):
    sorry_channel = bot.get_channel(916044583870267393)
    await ctx.defer()
    print('transforming ' + reason + ' into an apology video')
    if not (ctx.interaction):
      await ctx.reply('Processing... [this usually takes about 2 minutes...]')
    ID = gen_ID(4)
    try:
        await create_video(True, ID, reason)
    except Exception as e:
        if (len(str(e)) + 15 > 2000):
          print(str(e))
        else:
          await ctx.send(f'Whoopsie {ctx.author.mention}, I suffered a *' + str(e) + '* error, I\'ll try again now')
        try:
            await create_video(True, ID, reason)
            message = await ctx.reply(f'{ctx.author.mention} Your apology video is finished! Enjoy!',
                   file=discord.File("Finished/apology" + ID + ".mp4"))
            await updown(message)
            message2 = await sorry_channel.send(reason, file=discord.File("Finished/apology" + ID + ".mp4")) # back up the apology videos
            await updown(message2) # honestly this is really unnecessary but #consistency
        except Exception as e:
            ctx.send(
                f'*{str(e)}* is just too powerful {ctx.author.mention}. I was unable to produce your video, I suppose I now need to make an apology video of my own')
    os.remove("Finished/apology" + ID + ".mp4")

@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title='Help!',
                          color=discord.Color(6345206))
    embed.add_field(name='**s!sorry (reason)**',
                    value='Use s!sorry to create your own apology!',
                    inline=False)
    embed.add_field(name='**s!vc (reason)**',
                    value='Use s!vc to have sorrybot join vc and read aloud an apology!',
                    inline=False)
    await ctx.channel.send(embed=embed)

if __name__ == '__main__':
    bot.load_extension('voice')
    bot.run(TOKEN)
