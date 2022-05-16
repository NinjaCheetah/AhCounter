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
from discord.ext import commands
import platform


class Help(commands.Cog):
    """
    Basic help command embeds.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='help', help='Shows this message', invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Ah Counter Commands", color=0xffff00)
        embed.set_author(name="Ah Counter Help")
        embed.add_field(name="about", value="Shows info about the bot.", inline=False)
        embed.add_field(name="count", value="Shows the counts for all words.", inline=False)
        embed.add_field(name="milestones", value="Shows the milestones that count messages are sent at.", inline=False)
        embed.set_footer(text="Prefix is `$`")
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
        embed.add_field(name=":computer: Host:", value="Raspberry Pi 3B", inline=True)
        embed.add_field(name="Creator:", value="NinjaCheetah", inline=False)
        embed.add_field(name=":snake: Python version:", value=platform.python_version())
        embed.add_field(name="Bot version:", value="v1.6")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
