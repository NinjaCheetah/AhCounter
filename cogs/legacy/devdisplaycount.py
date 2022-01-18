# displaycount.py
import os
import random
from dotenv import load_dotenv
import discord
from discord.ext import commands
import io
import re
from discord.utils import get
import json

def load_devcounters():
    with open('devcounters.json', 'r') as f:
       devcounters = json.load(f)
    return devcounters

def save_devcounters(devcounters):
    with open('devcounters.json', 'w') as f:
       json.dump(devcounters, f)

class ShowCount(commands.Cog):
    """
    Commands to display counts for counted words.
    """
    def __init__(self, client):
        self.client = client

    @commands.command(name='ahcount', help='Displays the current number of Ahs')
    async def ahcount(self, message):
        counters = load_devcounters()
        await message.channel.send("A̶̘͓̹̋̔̓h̵͆̍͌͗̑ͅ Count: "+str(counters["Ah"]))
    @commands.command(name='bruhcount', help='Displays the current number of Bruhs')
    async def bruhcount(self, message):
        counters = load_devcounters()
        await message.channel.send("B̴̘͛r̵̪̾́͜u̶̡̦̤̎̍ḧ̴͇̭͛ Count: "+str(counters["Bruh"]))
    @commands.command(name='oofcount', help='Displays the current number of Oofs')
    async def oofcount(self, message):
        counters = load_devcounters()
        await message.channel.send("O̶͍̦̬̊ȍ̶̧̡̥͍̟͊̌͊͘f̴̟́͒͋ Count: "+str(counters["Oof"]))
    @commands.command(name='tonguecount', help='Displays the current number of ;Ps')
    async def tonguecount(self, message):
        counters = load_devcounters()
        await message.channel.send(";̴̨͔̥͑̿̂P̶̥͌̆̀ Count: "+str(counters[";P"]))
    @commands.command(name='ohcount', help='Displays the current number of Ohs')
    async def ohcount(self, message):
        counters = load_devcounters()
        await message.channel.send("O̸̱͂̑̈́h̶̙̞̞̓ Count: "+str(counters["Oh"]))

    @commands.command(name='devcountall', help='Displays the counts from all word counters.')
    async def devcountall(self, message):
        counters = load_devcounters()
        await message.channel.send("**Counting all the words!**")
        await message.channel.send("A̶̘͓̹̋̔̓h̵͆̍͌͗̑ͅ Count: "+str(counters["Ah"]) +"\nB̴̘͛r̵̪̾́͜u̶̡̦̤̎̍ḧ̴͇̭͛ Count: "+str(counters["Bruh"]) +"\nO̶͍̦̬̊ȍ̶̧̡̥͍̟͊̌͊͘f̴̟́͒͋ Count: "+str(counters["Oof"]) +"\n;̴̨͔̥͑̿̂P̶̥͌̆̀ Count: "+str(counters[";P"]) +"\nO̸̱͂̑̈́h̶̙̞̞̓ Count: "+str(counters["Oh"]))

    @commands.command(name='devmilestones')
    async def devmilestones(self, ctx):
        await ctx.send('Milestones: `10, 25, 50, 75, 100`\nMessage format: :trophy: Milestone! Count: <count>')

def setup(bot):
    bot.add_cog(ShowCount(bot))
