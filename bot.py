# bot.py
import asyncio
import os
import json
import discord
from discord.ext import commands

with open('config.json', 'r') as f:
    config = json.load(f)

TOKEN = config["TOKEN"]
# GUILD = config["GUILD"]

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

if not os.path.exists('counters.json'):
    os.mknod('counters.json')
    with open('counters.json', 'a') as f:
        f.write('{"Ah": {"regex": "ah","display": "Ah","count": 0}')

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
        await ctx.send(":white_check_mark: Loaded `cogs."+extension+"`")
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        await ctx.send(":warning: Failed to load extension `{}`\n```\n{}\n```".format(extension, exc))

@bot.command(name='unload', help='Unloads an extension.')
@commands.is_owner()
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.send(":white_check_mark: Unloaded `cogs."+extension+"`")

@bot.command(name='reload', help='Reloads an extension.')
@commands.is_owner()
async def reload(ctx, extension):
    try:
        await bot.reload_extension(f'cogs.{extension}')
        await ctx.send(":repeat: Reloaded `cogs."+extension+"`")
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        await ctx.send(":warning: Failed to reload extension `{}`\n```\n{}\n```".format(extension, exc))

@bot.command(name='reloadall', help='Reloads all extensions.')
@commands.is_owner()
async def reloadall(ctx):
    for extension in startup_extensions:
        try:
            await bot.reload_extension(extension)
            await ctx.send(":repeat: Reloaded `"+extension+"`")
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

@bot.event
async def on_ready():
    print('Ready.')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())
