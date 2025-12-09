# Ah Counter "management.py"
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

import logging
import re
import time

import discord
from discord import app_commands
from discord.ext import commands
import discord.utils

from config import BANNED_WORDS, BOT_MANAGERS, CONFIG
import dbinit


def check_slash_perms(interaction: discord.Interaction) -> bool:
    return interaction.user.id in BOT_MANAGERS or interaction.user.guild_permissions.manage_guild is True


def check_bot_manager(ctx) -> bool:
    return ctx.message.author.id in BOT_MANAGERS


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
        await message.edit(content=f":ping_pong: Ping: `{int(ping)}ms`")

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
        async with (self.bot.db.cursor() as cursor):
            for banned_word in BANNED_WORDS:
                if re.findall(f"\\b{banned_word}+\\b", new_word, re.IGNORECASE) \
                    or re.findall(f"\\b{banned_word}+\\b", new_regex, re.IGNORECASE):
                    await interaction.response.send_message(":warning: Sorry, that word/regex is not allowed.")
                    return
            sql = 'SELECT WORD FROM guild_counters WHERE GUILD_ID=?;'
            await cursor.execute(sql, (interaction.guild.id,))
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
                    (?, ?, ?, 0, ?)
                '''
                await cursor.execute(sql, (interaction.guild.id, new_word, new_regex, word_bound))
                await interaction.response.send_message(f":white_check_mark: Successfully added new word: `{new_word}`,"
                                                        f" with regex: `{new_regex}`!")
                logging.info("Added word \'%s\' with regex \'%s\' to guild \'%s\'", new_word, new_regex,
                             interaction.guild.name)

    @addword.error
    async def addword_err(self, interaction, error):
        await interaction.response.send_message(f":warning: {error} Please make sure you have the correct permissions "
                                                f"or are a bot manager.")

    @app_commands.command()
    @app_commands.check(check_slash_perms)
    async def delword(self, interaction: discord.Interaction, word: str):
        """Removes a word from the database"""
        async with self.bot.db.cursor() as cursor:
            for banned_word in BANNED_WORDS:
                if re.findall(f"\\b{banned_word}+\\b", word, re.IGNORECASE):
                    await interaction.response.send_message(":warning: Sorry, that input is not allowed.")
                    return
            guild_id = '{}'.format(interaction.guild.id)
            sql = 'SELECT WORD FROM guild_counters WHERE GUILD_ID=?;'
            await cursor.execute(sql, (guild_id,))
            word_list = [item for t in await cursor.fetchall() for item in t]
            for checked_word in word_list:
                if word.casefold() == checked_word.casefold():
                    sql = 'DELETE FROM guild_counters WHERE GUILD_ID=? AND WORD=?;'
                    await cursor.execute(sql, (guild_id, checked_word))
                    await self.bot.db.commit()
                    await interaction.response.send_message(f":white_check_mark: Successfully removed word: "
                                                            f"`{checked_word}`!")
                    logging.info("Removed word \'%s\' from \'%s\'", checked_word, interaction.guild.name)
                    return
            else:
                await interaction.response.send_message(":warning: That word is not in the database!")

    @delword.error
    async def delword_err(self, interaction, error):
        await interaction.response.send_message(f":warning: {error} Please make sure you have the correct permissions "
                                                f"or are a bot manager.")

    @app_commands.command()
    @app_commands.check(check_slash_perms)
    async def set_milestone_channel(self, interaction: discord.Interaction, channel_id_str: str):
        """Sets the milestone channel for the current server"""
        async with self.bot.db.cursor() as cursor:
            try:
                channel_id = int(channel_id_str.strip())
            except ValueError:
                await interaction.response.send_message(":warning: Please enter a valid channel ID.")
                return
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                await interaction.response.send_message(":warning: That channel could not be found!")
                return
            sql = 'UPDATE guild_settings SET MILESTONE_CHANNEL=? where GUILD_ID=?;'
            await cursor.execute(sql, (channel_id, interaction.guild.id))
            await self.bot.db.commit()
            if channel_id == 0:
                await interaction.response.send_message(f":white_check_mark: Milestone channel set to `{channel_id}`! "
                                                        f"Messages are now disabled.")
            elif channel_id == 1:
                await interaction.response.send_message(f":white_check_mark: Milestone channel set to `{channel_id}`! "
                                                        f"Messages will now be sent in the channel that they are "
                                                        f"triggered from.")
            else:
                await interaction.response.send_message(f":white_check_mark: Milestone channel set to <#{channel_id}>!")
            logging.info("Setting milestone channel for \'%s\' to %s", interaction.guild.name, channel_id)

    @set_milestone_channel.error
    async def set_milestone_channel_err(self, interaction, error):
        await interaction.response.send_message(f":warning: {error} Please make sure you have the correct permissions "
                                                f"or are a bot manager.")

    @commands.command(name='invite')
    async def invite(self, ctx):
        try:
            invite_url = CONFIG["INVITE"]
        except KeyError:
            logging.warning("Missing key 'INVITE' in config file!")
            await ctx.send("Sorry, this instance has no public invite link.")
            return
        if invite_url:
            await ctx.send(f"Invite me to your server using this link: {invite_url}")
        else:
            await ctx.send("Sorry, this instance has no public invite link.")


async def setup(bot):
    await bot.add_cog(Management(bot))
