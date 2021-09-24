import discord
from discord import member
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands


class av(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def av(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        embed = discord.Embed(
            title=f"{member.name}'s avatar", timestamp=ctx.message.created_at
        )

        embed.set_image(url=member.avatar_url)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(av(bot))
