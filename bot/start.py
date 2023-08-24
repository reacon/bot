import discord
import logging
import os
import requests
import json
import random
from discord.ext import commands

prefix = "-"
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())


@bot.command()
async def say(ctx, *, arg):
    await ctx.send(arg)


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    print(f"we have logged in as your mom")


@bot.command()
async def ping(ctx):
    embed = discord.Embed(
        color=discord.Colour.from_rgb(69, 42, 47), timestamp=ctx.message.created_at
    )
    embed.add_field(
        name="your moms ping pong",
        value=f"{round(bot.latency*1000)}mmyears ginku photography blonman go thicc bed wars :flushed:",  # profeshional strit komedyan
    )
    await ctx.send(embed=embed)

    


@bot.command()  # Description command
async def desc(ctx, *, random_stuff=None):
    """Description of the bot."""

    await ctx.send(">>> I love Ainz sama uwu")


# @bot.event
# async def on_message(message):
# if message.author == bot.user:
#    return

# if message.content.startswith("-hello"):
#    await message.channel.send("hello!")

formatter = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("nub.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

bot.run("ODg5MDMwOTc3Nzg2MTE0MDQ4.G_6Pl8.fNIbovduD0Xt5agBi3th8nBlptEpFS-w0vjZzw")  # our token
