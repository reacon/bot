import discord
import os
import requests
import json
import random
from discord.ext import commands

prefix="-"
bot = commands.Bot(command_prefix=prefix,intents=discord.Intents.all())

@bot.command()
async def say(ctx, *, arg):
    await ctx.send(arg)
    
@bot.command()
async def load(ctx,extension):
    bot.load_extension(f"cogs.{extension}")    
     

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f"we have logged in as {bot}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("-hello"):
        await message.channel.send("hello!")

bot.run("ODg5MDMwOTc3Nzg2MTE0MDQ4.YUbUng.O3KOp75dLyI96cj2n_4ARDS0Az8")
