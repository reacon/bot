import discord
from discord.ext import commands

from youtube_dl import YoutubeDL
import youtube_dl


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
        self.FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }

        self.vc = ""

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)[
                    "entries"
                ][0]
            except Exception:
                return False

        return {
            "source": info["formats"][0]["url"],
            "title": info["title"],
            "thumbnail": info["thumbnail"],
        }

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]["source"]

            self.music_queue.pop(0)
            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(),
            )

        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]["source"]

            if self.vc == "" or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])

            print(self.music_queue)
            self.music_queue.pop(0)
            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(),
            )
        else:
            self.is_playing = False

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def p(self, ctx, *args):
        query = "".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel == None:
            await ctx.send("enter a voice channel nub")
        else:
            song = self.search_yt(query)
            if not song:
                await ctx.send("could not download the song")
            else:

                embed = discord.Embed(
                    title="song added to queue", url=self.search_yt(query)["source"]
                )
                embed.set_author(
                    name="name suggestion pls", icon_url=self.bot.user.avatar_url
                )

                embed.set_thumbnail(url=self.search_yt(query)["thumbnail"])
                embed.set_footer(
                    text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url
                )

                await ctx.send(embed=embed)
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music()

    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        realshit = ""
        if not len(self.music_queue):
            await ctx.send("queue is empty")
            return

        for i in range(0, len(self.music_queue)):
            realshit += f"{i+1}" + "." + self.music_queue[i][0]["title"] + "\n"
        if realshit != "":
            await ctx.send(realshit)

    @commands.command(name="skip")
    async def skip1(self, ctx):
        if self.vc != "":
            self.vc.stop()
            await self.play_music()


def setup(bot):
    bot.add_cog(music(bot))
