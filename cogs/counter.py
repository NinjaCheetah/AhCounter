# Ah Counter "counter.py"
# Copyright (C) 2022  NinjaCheetah

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from discord.ext import commands
import json
import re
import unidecode
import asqlite

milestones = [10, 25, 50, 75, 100, 150, 200, 300, 400, 500, 1000, 1500, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
              10000]
sleepusers = []
sleepwords = ["tired", "bed", "rest"]
SLEEP_REGEX = [".?[s5xz\u0455]+.?.?[l1|]+.?.?[e3\u0435\u0395]+.?.?[e3\u0435\u0395]+.?.?[p\u0440\u03A1].?",
               ".?01010011.?01101100.?01100101.?01100101.?0111000.?"]

with open('config.json', 'r') as f:
    try:
        config = json.load(f)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Error loading config.json: {}'.format(exc))
MILESTONE_CHANNEL = config["MILESTONE_CHANNEL"]
try:
    for key in config["SLEEPUSERS"]:
        i = config["SLEEPUSERS"][key]
        sleepusers.append(int(i["ID"]))
except Exception as e:
    sleepusers = [0]


def has_sleep(string):
    match = re.search(SLEEP_REGEX[0], string, flags=re.IGNORECASE)
    if not match:
        string = unidecode.unidecode(string)
        match = re.search(SLEEP_REGEX[0], string, flags=re.IGNORECASE)
    return match


async def build_master_list(message, guild_id):
    async with asqlite.connect('counters.db') as db:
        async with db.cursor() as cursor:
            sql = 'SELECT ID FROM {}'
            await cursor.execute(sql.format("\"" + guild_id + "\""))
            id_list = [item for t in await cursor.fetchall() for item in t]
            sql = 'SELECT REGEX FROM {}'
            await cursor.execute(sql.format("\"" + guild_id + "\""))
            regex_strings = [item for t in await cursor.fetchall() for item in t]
            sql = 'SELECT WORD FROM {}'
            await cursor.execute(sql.format("\"" + guild_id + "\""))
            word_strings = [item for t in await cursor.fetchall() for item in t]
            sql = 'SELECT COUNT FROM {}'
            await cursor.execute(sql.format("\"" + guild_id + "\""))
            count_list = [item for t in await cursor.fetchall() for item in t]
            check_row_template = 'SELECT count(*) as tot FROM {}'
            await cursor.execute(check_row_template.format("\"" + guild_id + "\""))
            master_list = []
            for i in range(min(await cursor.fetchone())):
                master_list.append({"id": id_list[i], "word": word_strings[i], "regex": regex_strings[i],
                                    "count": count_list[i]})
    return master_list


class WordCounter(commands.Cog):
    """
    The code that handles counting words and saving them.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(name='count', help='Displays the counts from all word counters.')
    async def countall(self, message):
        async with asqlite.connect('counters.db') as db:
            async with db.cursor() as cursor:
                guild_id = '{}'.format(message.guild.id)
                master_list = await build_master_list(message, guild_id)
                wordcounts = ""
                await message.channel.send("**Counting all the words!**")
                for key in master_list:
                    wordcounts += "" + str(key["word"]) + " Count: " + str(key["count"]) + "\n"
                await message.channel.send(wordcounts)

    @commands.command(name='milestones')
    async def milestones(self, ctx):
        await ctx.send(
            "Milestones: `" + str(milestones) + "`\nMessage format: :trophy: Milestone reached! <word> Count: <count>")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None and message.author.id != 737755242757881937:
            async with asqlite.connect('counters.db') as db:
                async with db.cursor() as cursor:
                    guild_id = '{}'.format(message.guild.id)
                    master_list = await build_master_list(message, guild_id)
                    for key in master_list:
                        if re.findall("\\b" + str(key["regex"]) + "+\\b", message.content, re.IGNORECASE):
                            key["count"] += 1
                            if key["count"] in milestones:
                                await cursor.execute('SELECT MILESTONE_CHANNEL FROM guild_settings WHERE GUILD_ID == ?',
                                                     message.guild.id)
                                milestone_channel_tuple = [item for t in await cursor.fetchall() for item in t]
                                milestone_channel_id = int(min(milestone_channel_tuple))
                                milestone_channel = self.bot.get_channel(milestone_channel_id)
                                if not milestone_channel == 0:
                                    await message.milestone_channel.send(
                                        ":trophy: Milestone reached! " + str(key["word"]) + " Count: " + str(key["count"]))
                            sql = 'UPDATE {} set COUNT = {} where ID = ?'
                            await cursor.execute(sql.format("\""+guild_id+"\"", key["count"]), (key["id"],))
                            await db.commit()
        if message.author.id in sleepusers:
            if has_sleep(message.content):
                await message.add_reaction("🧢")
            else:
                for i in sleepwords:
                    if re.findall("\\b" + str(i) + "\\b", message.content, re.IGNORECASE):
                        await message.add_reaction("🧢")


async def setup(client):
    await client.add_cog(WordCounter(client))
