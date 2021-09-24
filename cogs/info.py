import discord
import os
from discord.ext import commands


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member

        roles = []
        for role in member.roles:
            roles += [role.mention]

        embed = discord.Embed(
            title=(f"info of {member}:"), timestamp=ctx.message.created_at
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="top role:", value=member.top_role.mention)
        embed.add_field(name="nickname:", value=member.display_name)
        embed.add_field(
            name="created at:",
            value=member.created_at.strftime("%a, %d %B %Y %H:%M:%S UTC"),
        )
        embed.add_field(
            name="joined server at:",
            value=member.joined_at.strftime("%a, %d %B %Y %H:%M:%S UTC"),
        )

        embed.add_field(
            name=f"Roles ({len(roles)})",
            value=",".join(roles),
        )
        embed.set_footer(
            text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(info(bot))
