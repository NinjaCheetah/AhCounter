# help.py
import discord
from discord.ext import commands

class Help(commands.Cog):
    """
    HALP!
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='help', help='Shows this message', invoke_without_command=True)
    async def help(self, ctx):
        embed=discord.Embed(title="Ah Counter Commands", color=0xffff00)
        embed.set_author(name="Ah Counter Help")
        embed.add_field(name="about", value="Shows info about the bot.", inline=False)
        embed.add_field(name="count", value="Shows the counts for all words.", inline=False)
        embed.add_field(name="milestones", value="Shows the milestones that count messages are sent at.", inline=False)
        embed.set_footer(text="Prefix is `$`")
        await ctx.send(embed=embed)

    @commands.group(name='ownerhelp', help='Shows this message', invoke_without_command=True)
    async def secrethelp(self, ctx):
        embed=discord.Embed(title="Owner-Only Management Commands", color=0xff0000)
        embed.set_author(name="Owner Help")
        embed.add_field(name="status", value="Use `$status set <message>` to set a status or `$status random` to pick a random one", inline=False)
        embed.add_field(name="load", value="Loads a cog", inline=True)
        embed.add_field(name="unload", value="Unloads a cog", inline=True)
        embed.add_field(name="reload", value="Reloads a cog", inline=True)
        embed.add_field(name="reloadall", value="Reloads all cogs", inline=True)
        embed.add_field(name="shutdown", value="Shuts down the bot", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))