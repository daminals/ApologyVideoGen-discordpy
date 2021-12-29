# bot.py
# Handles discord bot functionality
# Daniel Kogan, 06/01/2020

import os, sys
import discord, random, asyncio #now using pycord because discordpy no longer maintained
from dotenv import load_dotenv

load_dotenv()
from discord.ext import commands, tasks

TOKEN = os.environ.get('TOKEN', 3)
bot = commands.Bot(command_prefix='s!')
# TODO: add voice only support for VC

from sorry_engine import *

bot.remove_command('help')

async def updown(message):
    await message.add_reaction('<:upvote:776161705960931399>')
    await message.add_reaction('<:downvote:776162465842200617>')

@bot.event
async def on_ready():
    print('bot.py is active')
    servers = list(bot.guilds)
    server_num = len(servers)
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {server_num} servers| s!help"))

@bot.command(name='sorry')
async def sorry(ctx, *, sor):
    sorry_channel = bot.get_channel(916044583870267393)
    print('transforming ' + sor + ' into an apology video')
    await ctx.send('Processing... [this usually takes about 2 minutes...]')
    ID = gen_ID(4)
    
    try:
        await create_video(True, ID, sor)
    except Exception as e:
        await ctx.send(f'Whoopsie {ctx.author.mention}, I suffered a *' + str(e) + '* error, I\'ll try again now')
        try:
            await create_video(True, ID, sor)
        except Exception as e:
            ctx.send(
                f'*{str(e)}* is just too powerful {ctx.author.mention}. I was unable to produce your video, I suppose I now need to make an apology video of my own')
    message = await ctx.send(f'{ctx.author.mention} Your apology video is finished! Enjoy!',
                   file=discord.File("Finished/apology" + ID + ".mp4"))
    await updown(message)
    message2 = await sorry_channel.send(sor, file=discord.File("Finished/apology" + ID + ".mp4")) # back up the apology videos
    await updown(message2) # honestly this is really unnecessary but #consistency
    
    os.remove("Finished/apology" + ID + ".mp4")

@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title='Help!',
                          color=discord.Color(6345206))
    embed.add_field(name='**s!sorry (reason)**',
                    value='Use s!sorry to create your own apology!',
                    inline=False)
    await ctx.channel.send(embed=embed)

bot.load_extension('voice')

if __name__ == '__main__':
    bot.run(TOKEN)
