# Ah Counter "bot.py"
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
import asyncio
import discord
from discord.ext import commands
import asqlite
import logging

import dbinit
from config import CONFIG


TOKEN = CONFIG["TOKEN"]


class Bot(commands.Bot):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.db = None

    async def process_commands(self, message: discord.Message):
        ctx = await self.get_context(message)
        await self.invoke(ctx)


intents = discord.Intents.all()
bot = Bot(command_prefix='$', activity=discord.Game(name="Counting Ahs", type=3), intents=intents)
bot.remove_command('help')

startup_extensions = ["cogs.counter", "cogs.help", "cogs.management", "cogs.events"]


@bot.command(name='load', help='Loads an extension.')
@commands.is_owner()
async def load(ctx, extension):
    try:
        await bot.load_extension(f'cogs.{extension}')
        await ctx.send(":white_check_mark: Loaded `cogs." + extension + "`")
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        await ctx.send(":warning: Failed to load extension `{}`\n```\n{}\n```".format(extension, exc))
        logging.error(exc)


@bot.command(name='unload', help='Unloads an extension.')
@commands.is_owner()
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.send(":white_check_mark: Unloaded `cogs." + extension + "`")


@bot.command(name='reload', help='Reloads an extension.')
@commands.is_owner()
async def reload(ctx, extension):
    try:
        await bot.reload_extension(f'cogs.{extension}')
        await ctx.send(":repeat: Reloaded `cogs." + extension + "`")
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        await ctx.send(":warning: Failed to reload extension `{}`\n```\n{}\n```".format(extension, exc))
        logging.error(exc)


@bot.command(name='reloadall', help='Reloads all extensions.')
@commands.is_owner()
async def reloadall(ctx):
    for extension in startup_extensions:
        try:
            await bot.reload_extension(extension)
            await ctx.send(":repeat: Reloaded `" + extension + "`")
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await ctx.send(":warning: Failed to reload extension `{}`\n```\n{}\n```".format(extension, exc))
            logging.error(exc)


async def load_extensions():
    await bot.load_extension('jishaku')
    for extension in startup_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
            logging.error(exc)


@bot.event
async def on_ready():
    print("Ready!")
    logging.info("Bot is ready!")
    await dbinit.prepare_tables(bot)
    await dbinit.prepare_guild_settings(bot)
    await bot.tree.sync()


async def main():
    logging.basicConfig(filename="bot.log",
                        filemode='a',
                        format='%(asctime)s.%(msecs)03d:%(name)s:%(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)
    async with bot:
        bot.db = await asqlite.connect("counters.db")
        await load_extensions()
        await bot.start(TOKEN)


asyncio.run(main())
