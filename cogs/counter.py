# counter.py
import os
import discord
from discord.ext import commands
import discord.utils
import json
import re
import time
from dotenv import load_dotenv

milestones = [10,25,50,75,100,150,200,300,400,500,1000,1500,2000,3000,4000,5000,6000,7000,8000,9000,10000]
sleepusers = [327757456673472523, 644449298087411732]

load_dotenv()
MILESTONE_CHANNEL = os.getenv('MILESTONE_CHANNEL')

def load_counters():
    with open('counters.json', 'r') as f:
       counters = json.load(f)
    return counters

def save_counters(counters):
    with open('counters.json', 'w') as f:
       json.dump(counters, f)

class Message_Counter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='count', help='Displays the counts from all word counters.')
    async def countall(self, message):
        counters = load_counters()
        await message.channel.send("**Counting all the words!**")
        await message.channel.send("Ah Count: "+str(counters["Ah"]) +"\nBruh Count: "+str(counters["Bruh"]) +"\nOof Count: "+str(counters["Oof"]) +"\n;P Count: "+str(counters[";P"]) +"\nOh Count: "+str(counters["Oh"]) +"\nSims Count: "+str(counters["Sims"]) +"\nPog Count: "+str(counters["Pog"]))

    @commands.command(name='milestones')
    async def milestones(self, ctx):
        await ctx.send("Milestones: `" + str(milestones) + "`\nMessage format: :trophy: Milestone! Count: <count>")

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.client.get_channel(MILESTONE_CHANNEL)
        if message.guild != None:
            if re.findall("\\bah+\\b", message.content, re.IGNORECASE):
                counters = load_counters()
                counters["Ah"] += 1
                if counters["Ah"] in milestones:
                    await channel.send(":trophy: Milestone! Ah Count: "+str(counters["Ah"]))
                save_counters(counters)
            elif re.findall("\\bbruh+\\b", message.content, re.IGNORECASE):
                counters = load_counters()
                counters["Bruh"] += 1
                if counters["Bruh"] in milestones:
                    await channel.send(":trophy: Milestone! Bruh Count: "+str(counters["Bruh"]))
                save_counters(counters)
            elif re.findall(r"(:|;)p", message.content, re.IGNORECASE):
                counters = load_counters()
                counters[";P"] += 1
                if counters[";P"] in milestones:
                    await channel.send(":trophy: Milestone! ;P Count: "+str(counters[";P"]))
                save_counters(counters)
            elif ":winktongue:" in message.content:
                counters = load_counters()
                counters[";P"] += 1
                if counters[";P"] in milestones:
                    await channel.send(":trophy: Milestone! ;P Count: "+str(counters[";P"]))
                save_counters(counters)
            elif re.findall("\\boo+f+\\b", message.content, re.IGNORECASE):
                counters = load_counters()
                counters["Oof"] += 1
                if counters["Oof"] in milestones:
                    await channel.send(":trophy: Milestone! Oof Count: "+str(counters["Oof"]))
                save_counters(counters)
            elif re.findall("\\boh+\\b", message.content, re.IGNORECASE):
                counters = load_counters()
                counters["Oh"] += 1
                if counters["Oh"] in milestones:
                    await channel.send(":trophy: Milestone! Oh Count: "+str(counters["Oh"]))
                save_counters(counters)
            elif re.findall("\\bsims+\\b", message.content, re.IGNORECASE):
                counters = load_counters()
                counters["Sims"] += 1
                if counters["Sims"] in milestones:
                    await channel.send(":trophy: Milestone! Sims Count: "+str(counters["Sims"]))
                save_counters(counters)
            elif re.findall("\\bpog\\b", message.content, re.IGNORECASE):
                counters = load_counters()
                counters["Pog"] += 1
                if counters["Pog"] in milestones:
                    await channel.send(":trophy: Milestone! Pog Count: "+str(counters["Pog"]))
                save_counters(counters)
            if message.author.id in sleepusers:
                if re.findall(r"\**_*[s$§ßśŝš5zxｓ*]+\**[l1iIīłïîíìĺł\)\]\}\(\[\{|¡!ｌ*]+\**[e3èé€êēęë&ｅ*]+\**[p¶ｐ*]+_*\**", message.content, re.IGNORECASE):
                    await message.add_reaction("🧢")
                elif re.findall("\\bbed\\b", message.content, re.IGNORECASE):
                    await message.add_reaction("🧢")
                elif re.findall("\\btired\\b", message.content, re.IGNORECASE):
                    await message.add_reaction("🧢")

def setup(client):
    client.add_cog(Message_Counter(client))
