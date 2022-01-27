# devcounter.py
import os
import discord
from discord.ext import commands
import discord.utils
import json
import re
import unidecode

dev_milestones = [10,25,50,75,100,150,200,300,400,500,1000,1500,2000,3000,4000,5000,6000,7000,8000,9000,10000]
sleepusers = []
sleepwords = ["tired", "bed", "rest"]
SLEEP_REGEX = ".?[sxz\u0455]+.?.?[l1|]+.?.?[e3\u0435\u0395]+.?.?[e3\u0435\u0395]+.?.?[p\u0440\u03A1].?"

with open('config.json', 'r') as f:
    try:
        config = json.load(f)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Error loading config.json: {}'.format( exc))
MILESTONE_CHANNEL = config["MILESTONE_CHANNEL"]
try:
    for key in config["SLEEPUSERS"]:
        i = config["SLEEPUSERS"][key]
        sleepusers.append(int(i["ID"]))
except Exception as e:
    sleepusers = [0]

def load_devcounters():
    with open('devcounters.json', 'r') as f:
       counters = json.load(f)
    return counters

def save_devcounters(counters):
    with open('devcounters.json', 'w') as f:
       json.dump(counters, f, indent=4)

def has_sleep(string):
    match = re.search(SLEEP_REGEX, string, flags=re.IGNORECASE)
    if not match:
        string = unidecode.unidecode(string)
        match = re.search(SLEEP_REGEX, string, flags=re.IGNORECASE)
    return match

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
        await ctx.send("Milestones: `" + str(dev_milestones) + "`\nMessage format: :trophy: Milestone reached! <word> Count: <count>")

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.client.get_channel(MILESTONE_CHANNEL)
        if message.guild != None and message.author.id != 737755242757881937:
            counters = load_devcounters()
            for key in counters:
                i = counters[key]
                if re.findall("\\b"+str(i["regex"])+"+\\b", message.content, re.IGNORECASE):
                    i["count"] += 1
                    if i["count"] in milestones:
                        if not channel == 0:
                            await message.channel.send(":trophy: Milestone reached! "+str(i["display"])+" Count: "+str(i["count"]))
                save_devcounters(counters)
            if message.author.id in sleepusers:
                if has_sleep(message.content):
                    await message.add_reaction("🧢")
                else:
                    for i in sleepwords:
                        if re.findall("\\b"+str(i)+"\\b", message.content, re.IGNORECASE):
                            await message.add_reaction("🧢")

def setup(client):
    client.add_cog(DevMessage_Counter(client))