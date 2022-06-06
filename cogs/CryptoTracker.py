import random
import requests
from discord.ext import commands


class CryptoTracker(commands.Cog):

    def __int__(self, client):
        self.client = client

    def getCryptoPrice(self, crypto):
        db = {}
        URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
        r = requests.get(URL)
        data = r.json()
        for i in range(10):
            db[data[i]['id']] = data[i]['current_price']
        return db[crypto]

    def getAllCryptoPrices(self):
        db = {}
        URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
        r = requests.get(URL)
        data = r.json()
        for i in range(10):
            db[data[i]['id']] = data[i]['current_price']
        return db

    @commands.command()
    async def getAll(self, message):
        data = self.getAllCryptoPrices()
        for key, value in data.items():
            await message.channel.send(f"Current price of {key} is {value} $")

    @commands.command()
    async def cryptohelp(self, message):
        await message.channel.send("How to use the cryptoTrack"
                                   "\n getAll --> print out top 10 coin currently with their prices you can type coin name and get price like: "
                                   "\nbitcoin --> Current price of bitcoin is 29543 $"
                                   "\nsolana --> Current price of solana is 44.5 $")

    @commands.Cog.listener()
    async def on_message(self, message):
        # get selected coins current price
        data = self.getAllCryptoPrices()

        if message.content in data.keys():
            try:
                await message.channel.send(f"Current price of {message.content} is {data[message.content]} $")
            except:
                pass


def setup(client):
    client.add_cog(CryptoTracker(client))
