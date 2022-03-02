import discord
from discord.ext import commands
import discord.utils
import json
import time
import random

def load_devcounters():
    with open('devcounters.json', 'r') as f:
       devcounters = json.load(f)
    return devcounters

def save_devcounters(devcounters):
    with open('devcounters.json', 'w') as f:
       json.dump(devcounters, f, indent=4)

class Management(commands.Cog):
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
        await ctx.send(":x: Use `$status set <message>` to set status message, or if you are indecisive then use `$status random`.")

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
        num_words = random.randrange(3,6)
        status_string = ""
        for i in range(num_words):
            status_string += str(random.choice(status_word_list)).strip()+" "
        activity = discord.Game(name=status_string, type=3)
        await self.bot.change_presence(activity=activity)
        await ctx.send(":white_check_mark: Set status to: `" + status_string + "`")

    @commands.command(name="about")
    async def about(self, ctx):
        embed=discord.Embed(title="Ah Counter", color=0x00ff00)
        embed.set_author(name="About")
        embed.add_field(name=":computer: Host:", value="Raspberry Pi 3B", inline=True)
        embed.add_field(name="Creator:", value="NinjaCheetah", inline=False)
        embed.add_field(name=":snake: Python version:", value="3.9.9")
        embed.add_field(name="Bot version:", value="v1.5")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send(":electric_plug: Shutting down...")
        await ctx.bot.logout()

def setup(bot):
    bot.add_cog(Management(bot))
