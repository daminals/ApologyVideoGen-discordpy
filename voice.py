# sorry.py
# 12.29.2021

import discord, random, os
from discord.ext import commands
from sorry_engine import *
from bot import updown

class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('sorry.py is active')
                

def setup(bot):
    bot.add_cog(voice(bot))