import os

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="", intents=intents)
client.remove_command("help")


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


initial_extensions = []

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == "__main__":
    for extension in initial_extensions:
        client.load_extension(extension)

Token = "OTcwMzQ0NjIzNTY4NDY2MDMx.GOTnPo.OBYgbxn3Okr65NkYnf6QOomwKWD7OeKniUK0i8"
client.run(Token)
