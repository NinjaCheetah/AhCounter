# bot.py
import os
import random
from dotenv import load_dotenv
import discord
from discord.ext import commands
import io
import re
from discord.utils import get
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='$')

client = discord.Client

bot.remove_command('help')

startup_extensions = ["cogs.counter", "cogs.help", "cogs.management"]

bot.load_extension('jishaku')

if not os.path.exists('counters.json'):
    os.mknod('counters.json')
    with open('counters.json', 'a') as f:
        f.write('{"Ah": 0, "Bruh": 0, ";P": 0, "Oof": 0, "Oh": 0, "Sims": 0, "Pog": 0}')

if not os.path.exists('devcounters.json'):
    os.mknod('devcounters.json')
    with open('devcounters.json', 'a') as f:
        f.write('{"Ah": 0, "Bruh": 0, ";P": 0, "Oof": 0, "Oh": 0, "Sims": 0, "Pog": 0}')

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
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(":white_check_mark: Loaded `cogs."+extension+"`")
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        await ctx.send(":warning: Failed to load extension `{}`\n```\n{}\n```".format(extension, exc))

@bot.command(name='unload', help='Unloads an extension.')
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(":white_check_mark: Unloaded `cogs."+extension+"`")

@bot.command(name='reload', help='Reloads an extension.')
@commands.is_owner()
async def reload(ctx, extension):
    try:
        bot.reload_extension(f'cogs.{extension}')
        await ctx.send(":repeat: Reloaded `cogs."+extension+"`")
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        await ctx.send(":warning: Failed to reload extension `{}`\n```\n{}\n```".format(extension, exc))

@bot.command(name='reloadall', help='Reloads all extensions.')
@commands.is_owner()
async def reloadall(ctx):
    for extension in startup_extensions:
        try:
            bot.reload_extension(extension)
            await ctx.send(":repeat: Reloaded `"+extension+"`")
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await ctx.send(":warning: Failed to reload extension `{}`\n```\n{}\n```".format(extension, exc))

@bot.event
async def on_ready():
    print('Ready.')
    activity = discord.Game(name="Counting Ahs", type=3)
    await bot.change_presence(activity=activity)

def load_counters(self):
        with open('counters.json', 'r') as f:
            counters = json.load(f)
        return counters

def save_counters(self, counters):
    with open('counters.json', 'w') as f:
        json.dump(counters, f)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.run(TOKEN)
