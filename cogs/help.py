# Ah Counter "help.py"
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
import jishaku
from discord.ext import commands
from discord import app_commands
import platform
import sqlite3


class Help(commands.Cog):
    """
    Basic help command embeds.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='help', help='Shows this message', invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Ah Counter Commands", color=0x9702C5)
        embed.set_author(name="Ah Counter Help")
        embed.add_field(name="`$about`", value="Shows info about the bot.", inline=False)
        embed.add_field(name="`$count`", value="Shows the counts for all words.", inline=False)
        embed.add_field(name="`/count <word>`", value="Shows the count of the specified word.", inline=False)
        embed.add_field(name="`$invite`", value="Shows the invite link for this instance, if available.", inline=False)
        embed.add_field(name="`$milestones`", value="Shows the milestones that count messages are sent at.",
                        inline=False)
        embed.set_footer(text="Looking for configuration commands? Try /config_help.")
        await ctx.send(embed=embed)

    @commands.group(name='ownerhelp', help='Shows this message', invoke_without_command=True)
    async def secrethelp(self, ctx):
        embed = discord.Embed(title="Owner-Only Management Commands", color=0xff0000)
        embed.set_author(name="Owner Help")
        embed.add_field(name="status",
                        value="Use `$status set <message>` to set a status or `$status random` to pick a random one",
                        inline=False)
        embed.add_field(name="load", value="Loads a cog", inline=True)
        embed.add_field(name="unload", value="Unloads a cog", inline=True)
        embed.add_field(name="reload", value="Reloads a cog", inline=True)
        embed.add_field(name="reloadall", value="Reloads all cogs", inline=True)
        embed.add_field(name="shutdown", value="Shuts down the bot", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="about")
    async def about(self, ctx):
        embed = discord.Embed(title="Ah Counter", color=0x00ff00)
        embed.set_author(name="About")
        embed.add_field(name=":bust_in_silhouette: Creator:", value="NinjaCheetah", inline=True)
        embed.add_field(name=":globe_with_meridians: Website", value="[ncxprogramming.com]"
                             "(https://ncxprogramming.com/programs/ahcounter)", inline=True)
        embed.add_field(name=":keyboard: Source:", value="[GitHub](https://github.com/NinjaCheetah/AhCounter)")
        embed.add_field(name=":snake: Python version:", value=platform.python_version(), inline=True)
        embed.add_field(name=":clipboard: Database:", value="SQLite "+sqlite3.sqlite_version, inline=True)
        embed.add_field(name="Jishaku Version:", value=jishaku.__version__, inline=True)
        embed.add_field(name="Bot version:", value="v2.2.4", inline=False)
        embed.set_footer(text="Made with discord.py")
        await ctx.send(embed=embed)

    @app_commands.command()
    async def config_help(self, interaction=discord.Interaction):
        """Shows how to configure Ah Counter"""
        embed = discord.Embed(title="Ah Counter Configuration", color=0x280697)
        embed.set_author(name="Config Help")
        embed.add_field(name="`/addword <word> <regex>`", value="Adds a new word that will be counted and the regex"
                        " that will be used to detect it.", inline=False)
        embed.add_field(name="`/delword <word>`", value="Deletes the specified word and stops it from being counted."
                        " This cannot be undone!", inline=False)
        embed.add_field(name="`/set_milestone_channel`", value="Specify a channel for milestone messages to be sent to"
                        " using its channel ID. You can also set `0` to disable milestone messages, or `1` to send them"
                        " to the channel they were triggered from.", inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
