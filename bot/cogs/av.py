import discord
from discord import member
from discord.ext import commands


class av(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def av(self, ctx, member: discord.Member = None):

        if member is None:
            embed1 = discord.Embed(title="fdndjn", timestamp=ctx.message.created_at)
            await ctx.send(embed=embed1)
            return

        else:
            embed2 = discord.Embed(
                title="f'{member}'s avatar", timestamp=ctx.message.created_at
            )
            embed2.add_field(name="jdfjf", value=member.is_av_animated())
            embed2.set_image(url=member.util_url)
            await ctx.send(embed=embed2)


def setup(bot):
    bot.add_cog(av(bot))
