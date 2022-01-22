# counter.py
import os
import discord
from discord.ext import commands
import discord.utils
import json
import re
import unidecode

milestones = [10,25,50,75,100,150,200,300,400,500,1000,1500,2000,3000,4000,5000,6000,7000,8000,9000,10000]
sleepusers = []
sleepwords = ["tired", "bed", "rest"]
SLEEP_REGEX = ".?[sxz]+.?.?[l1|]+.?.?[e3]+.?.?[e3]+.?.?[p].?"

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

def load_counters():
    with open('counters.json', 'r') as f:
       counters = json.load(f)
    return counters

def save_counters(counters):
    with open('counters.json', 'w') as f:
       json.dump(counters, f, indent=4)

def has_sleep(string):
    string = unidecode.unidecode(string)
    match = re.search(SLEEP_REGEX, string, flags=re.IGNORECASE)
    return match

class Message_Counter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='count', help='Displays the counts from all word counters.')
    async def countall(self, message):
        counters = load_counters()
        await message.channel.send("**Counting all the words!**")
        wordcounts = ""
        for key in counters:
            i = counters[key]
            wordcounts += ""+str(i['display'])+" Count: "+str(i['count'])+"\n"
        await message.channel.send(wordcounts)

    @commands.command(name='milestones')
    async def milestones(self, ctx):
        await ctx.send("Milestones: `" + str(milestones) + "`\nMessage format: :trophy: Milestone! Count: <count>")

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.client.get_channel(MILESTONE_CHANNEL)
        if message.guild != None and message.author.id != 737755242757881937:
            counters = load_counters()
            for key in counters:
                i = counters[key]
                if re.findall("\\b"+str(i["regex"])+"+\\b", message.content, re.IGNORECASE):
                    i["count"] += 1
                save_counters(counters)
            if message.author.id in sleepusers:
                if has_sleep(message.content):
                    await message.add_reaction("🧢")
                else:
                    for i in sleepwords:
                        if re.findall("\\b"+str(i)+"\\b", message.content, re.IGNORECASE):
                            await message.add_reaction("🧢")

def setup(client):
    client.add_cog(Message_Counter(client))
