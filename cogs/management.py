# Ah Counter "management.py"
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
import discord
from discord import app_commands
from discord.ext import commands
import discord.utils
import time
import random
import asqlite


class Management(commands.Cog):
    """
    Management commands, such as setting the bot's status.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Gets the ping from the bot.')
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send(":ping_pong: Pinging...")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f":ping_pong: Ping:  `{int(ping)}ms`")

    @commands.group(name='status', invoke_without_command=True)
    @commands.is_owner()
    async def status(self, ctx):
        await ctx.send(":x: Use `$status set <message>` to set status message, or if you are indecisive then "
                       "use `$status random`.")

    @status.command(aliases=['Set', 'set', '-s', '-S'])
    @commands.is_owner()
    async def presence_set(self, ctx, *, message):
        activity = discord.Game(name=message, type=3)
        await self.bot.change_presence(activity=activity)
        await ctx.send(":white_check_mark: Set status message to: `" + message + "`")

    @status.command(aliases=['Classic', 'classic', '-c'])
    @commands.is_owner()
    async def status_random_classic(self, ctx):
        status_list = [
            'Counting Ahs',
            'Counting Bruhs',
            'Counting Oofs',
            'Counting ;Ps',
            'Counting Ohs',
            'BRUH',
            'generic status',
            'Bruh ;P',
            'NinjaCheetah and Rolfie are the best',
            'Joining forces with Universal-Bot',
            'Hmm...',
            ':thonk:',
            'Rolfie wuz here',
            'halp i need more status ideas',
            '🍎->👀();',
            'my status ideas are meeh at 3AM',
        ]
        response = random.choice(status_list)
        activity = discord.Game(name=response, type=3)
        await self.bot.change_presence(activity=activity)
        await ctx.send(":white_check_mark: Set status to: `" + response + "`")

    @status.command(aliases=['Random', 'random', '-r'])
    @commands.is_owner()
    async def status_random(self, ctx):
        with open("words.txt", "r") as f:
            status_word_list = f.readlines()
        num_words = random.randrange(3, 6)
        status_string = ""
        for i in range(num_words):
            status_string += str(random.choice(status_word_list)).strip() + " "
        status_string = status_string[:len(status_string) - 1]
        activity = discord.Game(name=status_string, type=3)
        await self.bot.change_presence(activity=activity)
        await ctx.send(":white_check_mark: Set status to: `" + status_string + "`")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send(":electric_plug: Shutting down...")
        await ctx.bot.logout()

    @app_commands.command()
    @commands.is_owner()
    async def addword(self, interaction: discord.Interaction, new_word: str, new_regex: str):
        """Adds a new word to the database"""
        async with asqlite.connect('counters.db') as db:
            async with db.cursor() as cursor:
                guild_id = '{}'.format(interaction.guild.id)
                sql = 'SELECT WORD FROM {}'
                await cursor.execute(sql.format("\"" + guild_id + "\""))
                word_list = [item for t in await cursor.fetchall() for item in t]
                if new_word not in word_list:
                    sql = 'SELECT ID FROM {}'
                    await cursor.execute(sql.format("\"" + guild_id + "\""))
                    id_list = [item for t in await cursor.fetchall() for item in t]
                    sql = '''
                        INSERT INTO {} 
                        (ID, WORD, REGEX, COUNT)
                        VALUES 
                        ({}, {}, {}, 0)
                    '''
                    await cursor.execute(sql.format("\"" + guild_id + "\"", max(id_list) + 1, "\"" + new_word + "\"",
                                                    "\"" + new_regex + "\""))
                    await interaction.response.send_message(":white_check_mark: Successfully added new word: `"
                                                            + new_word + "`, with regex: `" + new_regex + "`!")
                else:
                    await interaction.response.send_message(":warning: That word is already in the database!")

    @app_commands.command()
    @commands.is_owner()
    async def delword(self, interaction: discord.Interaction, word: str):
        """Removes a word from the database"""
        async with asqlite.connect("counters.db") as db:
            async with db.cursor() as cursor:
                guild_id = '{}'.format(interaction.guild.id)
                sql = 'SELECT WORD FROM {}'
                await cursor.execute(sql.format("\"" + guild_id + "\""))
                word_list = [item for t in await cursor.fetchall() for item in t]
                if word in word_list:
                    sql = 'DELETE from {} where WORD = {}'
                    await cursor.execute(sql.format("\"" + guild_id + "\"", "\"" + word + "\""))
                    await db.commit()
                    await interaction.response.send_message(":white_check_mark: Successfully removed word: `"
                                                            + word + "`!")
                else:
                    await interaction.response.send_message(":warning: That word is not in the database!")

    @app_commands.command()
    @commands.is_owner()
    async def set_milestone_channel(self, interaction: discord.Interaction, channel_id: str):
        """Sets the milestone channel for the current server"""
        async with asqlite.connect("counters.db") as db:
            async with db.cursor() as cursor:
                guild_id = '{}'.format(interaction.guild.id)
                try:
                    channel_id_int = int(channel_id.replace(" ", ""))
                except:
                    await interaction.response.send_message(":warning: Please enter a valid channel ID.")
                    return
                channel = self.bot.get_channel(channel_id_int)
                if channel is None:
                    await interaction.response.send_message(":warning: That channel could not be found!")
                elif channel == 0:
                    sql = 'UPDATE guild_settings set MILESTONE_CHANNEL = {} where GUILD_ID = ?'
                    await cursor.execute(sql.format(channel_id_int), (guild_id,))
                    await db.commit()
                    await interaction.response.send_message(":white_check_mark: Milestone channel set to `" +
                                                            channel_id.replace(" ", "") + "`! Messages are now "
                                                                                          "disabled.")
                else:
                    sql = 'UPDATE guild_settings set MILESTONE_CHANNEL = {} where GUILD_ID = ?'
                    await cursor.execute(sql.format(channel_id_int), (guild_id,))
                    await db.commit()
                    await interaction.response.send_message(":white_check_mark: Milestone channel set to <#" +
                                                            channel_id.replace(" ", "") + ">!")



async def setup(bot):
    await bot.add_cog(Management(bot))
