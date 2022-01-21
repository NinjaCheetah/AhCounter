# devcounter.py
import os
import discord
from discord.ext import commands
import discord.utils
import json
import re
import time

dev_milestones = [10,25,50,75,100,150,200,300,400,500,1000,1500,2000,3000,4000,5000,6000,7000,8000,9000,10000]
sleepusers = [327757456673472523, 644449298087411732]

def load_devcounters():
    with open('devcounters.json', 'r') as f:
       counters = json.load(f)
    return counters

def save_devcounters(counters):
    with open('devcounters.json', 'w') as f:
       json.dump(counters, f, indent=4)

class DevMessage_Counter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='devcount', help='Displays the counts from all word counters.')
    async def devcountall(self, message):
        counters = load_devcounters()
        await message.channel.send("**Counting all the words!**")
        wordcounts = ""
        for key in counters:
            i = counters[key]
            wordcounts += ""+str(i['display'])+" Count: "+str(i['count'])+"\n"
        await message.channel.send(wordcounts)

    @commands.command(name='devmilestones')
    async def devmilestones(self, ctx):
        await ctx.send('Milestones: `10, 25, 50, 75, 100`\nMessage format: :trophy: Milestone! Count: <count>')

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.client.get_channel(620406977490714626)
        if message.guild != None and message.author.id != 737755242757881937:
            counters = load_devcounters()
            for key in counters:
                i = counters[key]
                if re.findall("\\b"+str(i["regex"])+"+\\b", message.content, re.IGNORECASE):
                    i["count"] += 1
                save_devcounters(counters)
            if message.author.id in sleepusers:
                if re.findall(r"\**_*[s$§ßśŝš5zxｓ*]+\**[l1iIīłïîíìĺł\)\]\}\(\[\{|¡!ｌ*]+\**[e3èé€êēęë&ｅ*]+\**[p¶ｐ*]+_*\**", message.content, re.IGNORECASE):
                    await message.add_reaction("🧢")
                elif re.findall("\\bbed\\b", message.content, re.IGNORECASE):
                    await message.add_reaction("🧢")
                elif re.findall("\\btired\\b", message.content, re.IGNORECASE):
                    await message.add_reaction("🧢")

def setup(client):
    client.add_cog(DevMessage_Counter(client))
