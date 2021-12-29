# voice.py
# Daniel Kogan
# 12.29.2021

# The function of this cog is to connect to vc and read out an apology
import discord, random, os
from discord.ext import commands
from sorry_engine import *

class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('sorry.py is active')
        
    @commands.command(aliases=['voice'])
    async def vc(self, ctx, *, reason=None):
        vc_state = ctx.author.voice
        if not (vc_state):
            await ctx.reply("You are not currently in a vc")
            return False
        voice_channel = vc_state.channel
        # now that boilerplat is out of the way, we will create the audiofile
        audio_file = await create_audio(reason)
        connected_channel = await voice_channel.connect()
        connected_channel.play(discord.FFmpegPCMAudio(audio_file))
        await asyncio.sleep(audio_length(audio_file))
        await connected_channel.disconnect()
        # remove clutter
        os.remove(audio_file)
                
def setup(bot):
    bot.add_cog(voice(bot))