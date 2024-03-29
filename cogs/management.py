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
import logging
import re

import dbinit
from config import CONFIG
from config import BOT_MANAGERS
from config import BANNED_WORDS


def check_slash_perms(interaction: discord.Interaction) -> bool:
    return interaction.user.id in BOT_MANAGERS or interaction.user.guild_permissions.manage_guild is True


def check_bot_manager(ctx) -> bool:
    return ctx.message.author.id in BOT_MANAGERS


# noinspection DuplicatedCode
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
    @commands.check(check_bot_manager)
    async def status(self, ctx):
        await ctx.send(":x: Use `$status set <message>` to set status message, or if you are indecisive then "
                       "use `$status random`.")

    @status.command(aliases=['Set', 'set', '-s', '-S'])
    @commands.check(check_bot_manager)
    async def presence_set(self, ctx, *, message):
        activity = discord.Game(name=message, type=3)
        await self.bot.change_presence(activity=activity)
        await ctx.send(":white_check_mark: Set status message to: `" + message + "`")

    @status.command(aliases=['Classic', 'classic', '-c'])
    @commands.check(check_bot_manager)
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
    @commands.check(check_bot_manager)
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
    @commands.check(check_bot_manager)
    async def shutdown(self, ctx):
        logging.warning("Bot is shutting down!")
        await ctx.send(":electric_plug: Shutting down...")
        await self.bot.close()

    @commands.command()
    @commands.check(check_bot_manager)
    async def checkdb(self, ctx):
        message = await ctx.send("Re-initializing databases...")
        await dbinit.prepare_guild_settings(self.bot)
        await dbinit.prepare_tables(self.bot)
        await message.edit(content="Re-initializing databases... :white_check_mark:")

    @app_commands.command()
    @app_commands.check(check_slash_perms)
    async def addword(self, interaction: discord.Interaction, new_word: str, new_regex: str, word_bound: bool = True):
        """Adds a new word to the database"""
        async with self.bot.db.cursor() as cursor:
            for banned_word in BANNED_WORDS:
                if re.findall("\\b" + banned_word + "+\\b", new_word, re.IGNORECASE) or re.findall("\\b" + banned_word +
                                                                                                   "+\\b", new_regex,
                                                                                                   re.IGNORECASE):
                    await interaction.response.send_message(":warning: Sorry, that word/regex is not allowed.")
                    return
            guild_id = '{}'.format(interaction.guild.id)
            sql = 'SELECT WORD FROM guild_counters WHERE GUILD_ID=$1;'
            await cursor.execute(sql, guild_id)
            word_list = [item for t in await cursor.fetchall() for item in t]
            for checked_word in word_list:
                if new_word.casefold() == checked_word.casefold():
                    await interaction.response.send_message(":warning: That word is already in the database!")
                    return
            else:
                sql = '''
                    INSERT INTO guild_counters 
                    (GUILD_ID,WORD,REGEX,COUNT,WORDBOUND)
                    VALUES 
                    ($1, $2, $3, 0, $4)
                '''
                await cursor.execute(sql, guild_id, new_word, new_regex, word_bound)
                await interaction.response.send_message(":white_check_mark: Successfully added new word: `"
                                                        + new_word + "`, with regex: `" + new_regex + "`!")
                logging.info("Added word \'%s\' with regex \'%s\' to guild \'%s\'", new_word, new_regex,
                             interaction.guild.name)

    @addword.error
    async def addword_err(self, interaction, error):
        await interaction.response.send_message(":warning: " + str(error) + " Please make sure you have the correct"
                                                                            " permissions or are a bot manager.")

    @app_commands.command()
    @app_commands.check(check_slash_perms)
    async def delword(self, interaction: discord.Interaction, word: str):
        """Removes a word from the database"""
        async with self.bot.db.cursor() as cursor:
            for banned_word in BANNED_WORDS:
                if re.findall("\\b" + banned_word + "+\\b", word, re.IGNORECASE):
                    await interaction.response.send_message(":warning: Sorry, that input is not allowed.")
                    return
            guild_id = '{}'.format(interaction.guild.id)
            sql = 'SELECT WORD FROM guild_counters WHERE GUILD_ID=$1;'
            await cursor.execute(sql, guild_id)
            word_list = [item for t in await cursor.fetchall() for item in t]
            for checked_word in word_list:
                if word.casefold() == checked_word.casefold():
                    sql = 'DELETE FROM guild_counters WHERE GUILD_ID=$1 AND WORD=$2;'
                    await cursor.execute(sql, guild_id, checked_word)
                    await self.bot.db.commit()
                    await interaction.response.send_message(":white_check_mark: Successfully removed word: `"
                                                            + checked_word + "`!")
                    logging.info("Removed word \'%s\' from \'%s\'", checked_word, interaction.guild.name)
                    return
            else:
                await interaction.response.send_message(":warning: That word is not in the database!")

    @delword.error
    async def delword_err(self, interaction, error):
        await interaction.response.send_message(":warning: " + str(error) + " Please make sure you have the correct"
                                                                            " permissions or are a bot manager.")

    @app_commands.command()
    @app_commands.check(check_slash_perms)
    async def set_milestone_channel(self, interaction: discord.Interaction, channel_id: str):
        """Sets the milestone channel for the current server"""
        async with self.bot.db.cursor() as cursor:
            guild_id = '{}'.format(interaction.guild.id)
            try:
                channel_id_int = int(channel_id.replace(" ", ""))
            except ValueError:
                await interaction.response.send_message(":warning: Please enter a valid channel ID.")
                return
            channel = self.bot.get_channel(channel_id_int)
            sql = 'UPDATE guild_settings SET MILESTONE_CHANNEL=$1 where GUILD_ID=$2;'
            if channel_id_int == 0:
                await cursor.execute(sql, channel_id_int, guild_id)
                await self.bot.db.commit()
                await interaction.response.send_message(":white_check_mark: Milestone channel set to `" +
                                                        channel_id.replace(" ", "") + "`! Messages are now "
                                                                                      "disabled.")
            elif channel_id_int == 1:
                await cursor.execute(sql, channel_id_int, guild_id)
                await self.bot.db.commit()
                await interaction.response.send_message(":white_check_mark: Milestone channel set to `" +
                                                        channel_id.replace(" ", "") + "`! Messages will now "
                                                                                      "be sent in the channel they're "
                                                                                      "triggered from.")
            elif channel is None:
                await interaction.response.send_message(":warning: That channel could not be found!")
            else:
                await cursor.execute(sql, channel_id_int, guild_id)
                await self.bot.db.commit()
                await interaction.response.send_message(":white_check_mark: Milestone channel set to <#" +
                                                        channel_id.replace(" ", "") + ">!")
            logging.info("Setting milestone channel for \'%s\' to %s", interaction.guild.name, channel_id_int)

    @set_milestone_channel.error
    async def set_milestone_channel_err(self, interaction, error):
        await interaction.response.send_message(":warning: " + str(error) + " Please make sure you have the correct"
                                                                            " permissions or are a bot manager.")

    @commands.command(name='invite')
    async def invite(self, ctx):
        try:
            invite_url = CONFIG["INVITE"]
        except KeyError:
            logging.warning("Missing key 'INVITE' in config file!")
            await ctx.send("Sorry, this instance has no public invite link.")
            return
        if invite_url:
            await ctx.send("Invite me to your server using this link: " + invite_url)
        else:
            await ctx.send("Sorry, this instance has no public invite link.")


async def setup(bot):
    await bot.add_cog(Management(bot))
