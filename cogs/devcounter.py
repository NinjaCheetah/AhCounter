# devcounter.py
import discord
from discord.ext import commands
import discord.utils
import json
import re
import time

dev_milestones = [10,25,50,75,100,150,200,300,400,500,1000,1500,2000,3000,4000,5000,6000,7000,8000,9000,10000]

def load_devcounters():
    with open('devcounters.json', 'r') as f:
       counters = json.load(f)
    return counters

def save_devcounters(counters):
    with open('devcounters.json', 'w') as f:
       json.dump(counters, f)

class DevMessage_Counter(commands.Cog):
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

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.client.get_channel(620406977490714626)
        if message.guild != None:
            if re.findall("\\bah+\\b", message.content, re.IGNORECASE):
                counters = load_devcounters()
                counters["Ah"] += 1
                if counters["Ah"] in dev_milestones:
                    await channel.send(":trophy: Milestone! A̶̘͓̹̋̔̓h̵͆̍͌͗̑ͅ Count: "+str(counters["Ah"]))
                save_devcounters(counters)
            elif re.findall("\\bbruh+\\b", message.content, re.IGNORECASE):
                counters = load_devcounters()
                counters["Bruh"] += 1
                if counters["Bruh"] in dev_milestones:
                    await channel.send(":trophy: Milestone! B̴̘͛r̵̪̾́͜u̶̡̦̤̎̍ḧ̴͇̭͛ Count: "+str(counters["Bruh"]))
                save_devcounters(counters)
            elif re.findall(r"(:|;)p", message.content, re.IGNORECASE):
                counters = load_devcounters()
                counters[";P"] += 1
                if counters[";P"] in dev_milestones:
                    await channel.send(":trophy: Milestone! ;̴̨͔̥͑̿̂P̶̥͌̆̀ Count: "+str(counters[";P"]))
                save_devcounters(counters)
            elif ":winktongue" in message.content:
                counters = load_devcounters()
                counters[";P"] += 1
                if counters[";P"] in dev_milestones:
                    await channel.send(":trophy: Milestone! ;̴̨͔̥͑̿̂P̶̥͌̆̀ Count: "+str(counters[";P"]))
                save_devcounters(counters)
            elif re.findall("\\boo+f+\\b", message.content, re.IGNORECASE):
                counters = load_devcounters()
                counters["Oof"] += 1
                if counters["Oof"] in dev_milestones:
                    await channel.send(":trophy: Milestone! O̶͍̦̬̊ȍ̶̧̡̥͍̟͊̌͊͘f̴̟́͒͋ Count: "+str(counters["Oof"]))
                save_devcounters(counters)
            elif re.findall("\\boh+\\b", message.content, re.IGNORECASE):
                counters = load_devcounters()
                counters["Oh"] += 1
                if counters["Oh"] in dev_milestones:
                    await channel.send(":trophy: Milestone! O̸̱͂̑̈́h̶̙̞̞̓ Count: "+str(counters["Oh"]))
                save_devcounters(counters)

def setup(client):
    client.add_cog(DevMessage_Counter(client))
