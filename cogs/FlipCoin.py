import random

import discord
from discord.ext import commands

class FlipCoin(commands.Cog):

    def __int__(self, client):
        self.client = client

    @commands.command()
    async def flipcoin(self,ctx):
        heads_tails = ['Heads', 'Tails']
        choice = random.choice(heads_tails)
        await ctx.send(choice + " wins!")

    @commands.command()
    async def fliphelp(self, message):
        await message.channel.send("type [flip] for flipping coin"
                                   "\n flip --> Head wins or Tail win")


def setup(client):
    client.add_cog(FlipCoin(client))