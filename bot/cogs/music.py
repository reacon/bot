import discord
from discord.ext import commands

from youtube_dl import YoutubeDL
import youtube_dl


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        # self.vc = ""
        self.music_queue = {}
        self.FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }

    async def search_yt(self, item):
        with YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)[
                    "entries"
                ][0]
            except Exception:
                return False

            return info

    def play_next(self, ctx):
        if len(self.music_queue[ctx.guild.id]) > 0:
            self.is_playing = True

            s_url = self.music_queue[ctx.guild.id][0]["formats"][0]["url"]
            self.music_queue[ctx.guild.id].pop(0)

            self.vc.play(
                discord.FFmpegPCMAudio(s_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(ctx),
            )

        else:
            self.is_playing = False

    def play_music(self, ctx, song):
        if len(self.music_queue[ctx.guild.id]) > 0:
            self.is_playing = True
            s_url = self.music_queue[ctx.guild.id][0]["formats"][0]["url"]

            source = discord.FFmpegPCMAudio(s_url, **self.FFMPEG_OPTIONS)
            self.music_queue[ctx.guild.id].pop(0)

            self.vc = ctx.message.guild.voice_client
            self.vc.play(source, after=lambda e: self.play_next(ctx))

        else:
            self.is_playing = False

    @commands.command(name="c")
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send(
                "You are not connected to a voice channel, please connect to the channel you want the bot to join."
            )

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command(name="play")
    async def p(self, ctx, *args):
        query = "".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel == None:
            ctx.send("enter a vc nub")
        else:
            song = await self.search_yt(query)

            if not song:
                await ctx.send("could not download the song")
            else:

                if not ctx.guild.id in self.music_queue:
                    self.music_queue[ctx.guild.id] = []

                embed = discord.Embed(
                    title=f"{(await self.search_yt(query))['title']}",
                    url=(await self.search_yt(query))["formats"][0]["url"],
                )
                embed.set_author(
                    name="name suggestion pls", icon_url=self.bot.user.avatar_url
                )

                embed.set_thumbnail(url=(await self.search_yt(query))["thumbnail"])
                embed.set_footer(
                    text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url
                )

                self.music_queue[ctx.guild.id].append(song)
                await ctx.send(embed=embed)

                # try:
                #     self.play_music(ctx, song)
                # except:
                await voice_channel.connect()
                self.play_music(ctx, song)

                if self.is_playing == False:
                    self.play_music(ctx, song)

    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        queue_ = ""
        if not len(self.music_queue[ctx.guild.id]):
            await ctx.send("queue is empty")
            return
        for i in range(len(self.music_queue[ctx.guild.id])):
            queue_ += f"{i+1}" + "." + self.music_queue[ctx.guild.id][i]["title"] + "\n"
        if queue_ != "":
            await ctx.send(queue_)

    @commands.command(name="skip")
    async def skip1(self, ctx):
        if self.vc != "":
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="r")
    async def remove(self, ctx, index: int):
        if 1 <= index <= len(self.music_queue[ctx.guild.id]):
            self.music_queue[ctx.guild.id].pop(index - 1)
            await ctx.send(f"song {index} removed")
            await self.play_music(ctx)

    @commands.command(name="l")
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("I am not connected to a voice channel.")

    @commands.command(aliases=["np"])
    async def now_playing(self, ctx):
        pass


def setup(bot):
    bot.add_cog(music(bot))
