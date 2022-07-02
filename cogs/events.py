# Ah Counter "event.py"
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
import logging
import traceback

import dbinit


class Events(commands.Cog):
    """
    The code that handles counting words and saving them.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":x: You are missing a required argument!")
        elif isinstance(error, commands.ExtensionNotFound):
            await ctx.send(":x: That extension could not be found!")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(":x: You are missing the permissions required to run this command.")
        else:
            if not isinstance(error, commands.CommandNotFound):
                etype = type(error)
                trace = error.__traceback__
                lines = traceback.format_exception(etype, error, trace)
                traceback_text = ''.join(lines)
                await ctx.send(":no_entry: An error has occurred.\n```\n" + traceback_text + "```\n")
                logging.error(traceback_text)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logging.info("Joined new guild: %s", guild.name)
        await dbinit.prepare_guild_settings(self.client)
        await dbinit.prepare_tables(self.client)


async def setup(client):
    await client.add_cog(Events(client))
