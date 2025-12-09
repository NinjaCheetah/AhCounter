# Ah Counter "counter.py"
# Copyright (C) 2022-2025 NinjaCheetah

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

import re

import discord
from discord import app_commands
from discord.ext import commands


MILESTONES = [10, 25, 50, 75, 100, 150, 200, 300, 400, 500, 1000, 1500, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
              10000, 11000, 12000, 13000, 14000, 15000, 20000, 25000, 50000, 75000, 100000, 150000, 200000, 250000]


async def build_master_list(client, guild_id):
    async with client.db.cursor() as cursor:
        sql = 'SELECT ID FROM guild_counters WHERE GUILD_ID=?;'
        await cursor.execute(sql, (guild_id,))
        id_list = [item for t in await cursor.fetchall() for item in t]
        sql = 'SELECT REGEX FROM guild_counters WHERE GUILD_ID=?;'
        await cursor.execute(sql, (guild_id,))
        regex_strings = [item for t in await cursor.fetchall() for item in t]
        sql = 'SELECT WORD FROM guild_counters WHERE GUILD_ID=?;'
        await cursor.execute(sql, (guild_id,))
        word_strings = [item for t in await cursor.fetchall() for item in t]
        sql = 'SELECT COUNT FROM guild_counters WHERE GUILD_ID=?;'
        await cursor.execute(sql, (guild_id,))
        count_list = [item for t in await cursor.fetchall() for item in t]
        sql = 'SELECT WORDBOUND FROM guild_counters WHERE GUILD_ID=?'
        await cursor.execute(sql, (guild_id,))
        use_bounds = [item for t in await cursor.fetchall() for item in t]
        check_row_template = 'SELECT count(*) as tot FROM guild_counters WHERE GUILD_ID=?;'
        await cursor.execute(check_row_template, (guild_id,))
        master_list = []
        for i in range(min(await cursor.fetchone())):
            master_list.append({"id": id_list[i], "word": word_strings[i], "regex": regex_strings[i],
                                "count": count_list[i], "use_bounds": use_bounds[i]})
    return master_list


class WordCounter(commands.Cog):
    """
    The code that handles counting words and saving them.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(name='count', help='Displays the counts from all word counters.')
    async def countall(self, message):
        master_list = await build_master_list(self.client, message.guild.id)
        wordcounts = ""
        await message.channel.send("**Counting all the words!**")
        for key in master_list:
            wordcounts += f"{key["word"]} Count: {key["count"]}\n"
        await message.channel.send(wordcounts)

    @commands.command(name='milestones')
    async def milestones(self, ctx):
        await ctx.send(f"Milestones: `{MILESTONES}`\nMessage format: :trophy: Milestone reached! <word> Count: <count>")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None and message.author.id != 742827192362205267:
            async with self.client.db.cursor() as cursor:
                master_list = await build_master_list(self.client, message.guild.id)
                for key in master_list:
                    if not key["use_bounds"]:
                        regex_bounds = ["", ""]
                    else:
                        regex_bounds = ["\\b", ".*\\b"]
                    if re.findall(regex_bounds[0] + str(key["regex"]) + regex_bounds[1], message.content, re.IGNORECASE):
                        key["count"] += 1
                        if key["count"] in MILESTONES:
                            await cursor.execute('SELECT MILESTONE_CHANNEL FROM guild_settings WHERE GUILD_ID == ?',
                                                 (message.guild.id,))
                            milestone_channel_id = int(max([item for t in await cursor.fetchall() for item in t]))
                            if milestone_channel_id == 1:
                                await message.channel.send(
                                    ":trophy: Milestone reached! " + str(key["word"]) + " Count: " + str(key["count"]))
                            else:
                                channel = self.client.get_channel(milestone_channel_id)
                                if channel is not None:
                                    await channel.send(":trophy: Milestone reached! " + str(key["word"]) + " Count: " +
                                                       str(key["count"]))
                        sql = 'UPDATE guild_counters SET COUNT=? where ID=?'
                        await cursor.execute(sql, (key["count"], key["id"]))
                        await self.client.db.commit()

    @app_commands.command()
    async def countword(self, interaction: discord.Interaction, word: str):
        """Gets the count of a specific word"""
        master_list = await build_master_list(self.client, interaction.guild_id)
        word_list = []
        count = 0
        original_word = ""
        for key in master_list:
            word_list.append(key["word"].casefold())
            if word.casefold() in key["word"].casefold():
                count = key["count"]
                original_word = key["word"]
        if word.casefold() in word_list:
            await interaction.response.send_message(f"Count for word \"{original_word}\": {count}")
        else:
            await interaction.response.send_message(":warning: That word is not in the database!")


async def setup(client):
    await client.add_cog(WordCounter(client))
