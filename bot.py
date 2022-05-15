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
import json
import discord
from discord.ext import commands
import asqlite

with open('config.json', 'r') as f:
    config = json.load(f)

TOKEN = config["TOKEN"]


class Bot(commands.Bot):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    async def process_commands(self, message: discord.Message):
        ctx = await self.get_context(message)
        await self.invoke(ctx)


intents = discord.Intents.all()
bot = Bot(command_prefix='$', activity=discord.Game(name="Counting Ahs", type=3), intents=intents)
bot.remove_command('help')

startup_extensions = ["cogs.counter", "cogs.help", "cogs.management"]


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":x: You are missing a required argument!")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(":x: That command could not be found.")
    if isinstance(error, commands.ExtensionError):
        await ctx.send(":x: That extension could not be found!")
    if isinstance(error, commands.ExtensionNotLoaded):
        await ctx.send(":x: There was an error while loading that extension.")
    if isinstance(error, commands.ExtensionFailed):
        await ctx.send(":x: There was an error while loading that extension.")
    if isinstance(error, commands.ExtensionNotFound):
        await ctx.send(":x: That extension could not be found!")


@bot.command(name='load', help='Loads an extension.')
@commands.is_owner()
async def load(ctx, extension):
    try:
        await bot.load_extension(f'cogs.{extension}')
        await ctx.send(":white_check_mark: Loaded `cogs." + extension + "`")
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        await ctx.send(":warning: Failed to load extension `{}`\n```\n{}\n```".format(extension, exc))


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


async def load_extensions():
    await bot.load_extension('jishaku')
    for extension in startup_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


async def prepare_guild_settings():
    async with asqlite.connect('counters.db') as db:
        async with db.cursor() as cursor:
            sql = '''
                CREATE TABLE IF NOT EXISTS guild_settings
                    (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
                    GUILD_ID           INT    NOT NULL,
                    MILESTONE_CHANNEL           INT     NOT NULL)
            '''
            await cursor.execute(sql)
            sql = 'SELECT GUILD_ID FROM guild_settings'
            await cursor.execute(sql)
            guild_id_list = [item for t in await cursor.fetchall() for item in t]
            bot_guilds = bot.guilds
            for guild in bot_guilds:
                if guild.id not in guild_id_list:
                    sql = '''
                        INSERT INTO guild_settings 
                        (GUILD_ID,MILESTONE_CHANNEL)
                        VALUES ({}, 0)
                    '''
                    await cursor.execute(sql.format(guild.id))
            await db.commit()


async def prepare_tables():
    async with asqlite.connect('counters.db') as db:
        async with db.cursor() as cursor:
            bot_guilds = bot.guilds
            for guild in bot_guilds:
                guild_id = '{}'.format(guild.id)
                await cursor.execute('SELECT count(name) FROM sqlite_master WHERE type="table" AND name=? ', (guild_id,))
                if await cursor.fetchone() == 0:
                    sql = '''
                        CREATE TABLE {}
                            (ID INT PRIMARY KEY     NOT NULL,
                            WORD           TEXT    NOT NULL,
                            REGEX           TEXT     NOT NULL,
                            COUNT        INT            NOT NULL)
                    '''
                    await cursor.execute(sql.format("\""+guild_id+"\""))
                check_row_template = 'SELECT count(*) as tot FROM {}'
                await cursor.execute(check_row_template.format("\"" + guild_id + "\""))
                if not min(await cursor.fetchone()) > 0:
                    sql = '''
                        INSERT INTO {} 
                        (ID,WORD,REGEX,COUNT) 
                        VALUES 
                        (1, 'Ah', 'ah', 0 )
                    '''
                    await cursor.execute(sql.format("\""+guild_id+"\""))
                    await db.commit()


@bot.event
async def on_ready():
    print('Ready.')
    await prepare_tables()
    await prepare_guild_settings()


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


asyncio.run(main())
