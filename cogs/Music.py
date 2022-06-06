from discord.ext import commands
import discord, youtube_dl, os, asyncio


class Music(commands.Cog):

    def __int__(self, client, song_queue, delete_files):
        self.client = client
        self.song_queue = []
        self.delete_files = []

    @commands.command()  # method that converts provided function into a discord command
    async def join(self, ctx):  # join function
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def musichelp(self, message):
        await message.channel.send("After joining a voice channel in dc:"
                                   "\njoin : bot joins the channel"
                                   "\nplay (url or song name) : bot play the desired song"
                                   "\npause: pauses song"
                                   "\nresume: resumes song"
                                   "\nskip / !stop: skips if anything on the queue, else displays message “no song is on the queue”"
                                   "\nshowlist: shows the song queue to the user"
                                   "\nleave: bot leaves the channel")

    @commands.command()
    async def leave(self, ctx):  # leave function
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, word):  # 'word' parameter stands for the song name or link that user typed
        youtube_options = {}  # dictionary for options on youtube_dl library
        voice = ctx.voice_client

        if word[0:4] == "http" or word[0:3] == "www":  # option 1: if its a url
            with youtube_dl.YoutubeDL(youtube_options) as ydownload:
                videoinfo = ydownload.extract_info(word, download=False)  # finds url, gets info about video
                title = videoinfo["title"]
                url = word

        if word[0:4] != "http" and word[0:3] != "www":  # option 2: if its a name which is going to searched on youtube.
            with youtube_dl.YoutubeDL(youtube_options) as ydownload:
                videoinfo = ydownload.extract_info(f"ytsearch:{word}", download=False)["entries"][
                    0]  # searches for typed word in youtube
                title = videoinfo["title"]
                url = videoinfo["webpage_url"]

        youtube_options = {  # this part is settings for the youtube video to be downloaded
            'format': 'bestaudio/best',
            "outtmpl": f"{title}.mp3",  # to save it by the video name
            "postprocessors":
                [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
        }

        def download(url):  # download audio
            with youtube_dl.YoutubeDL(youtube_options) as ydownload:
                ydownload.download([url])

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, download, url)

        # song queue
        if voice.is_playing():
            self.song_queue.append(title)  # add song to the "song_queue" list
            await ctx.send(f" ** {title} ** --> is added to queue")  # displays this message for the user
        else:
            voice.play(discord.FFmpegPCMAudio(f"{title}.mp3"), after=lambda e: check_queue())
            await ctx.send(f":musical_note: ** {title} ** --> is playing now")  # displays this message for the user
            self.delete_files.append(title)

        def check_queue():
            try:
                if self.song_queue[0] != None:  # if it is any song on the queue, this block displays
                    voice.play(discord.FFmpegPCMAudio(f"{self.song_queue[0]}.mp3"), after=lambda e: check_queue())
                    self.delete_files.append(self.song_queue[0])
                    self.song_queue.pop(0)  # prevents repeating the same song over and over
            except IndexError:
                for file in self.delete_files:
                    os.remove(f"{file}.mp3")
                self.delete_files.clear()  # removes the downloaded song files after play

    @commands.command()
    async def pause(self, ctx):  # pause method
        if ctx.voice_client.is_playing() == True:
            ctx.voice_client.pause()
        else:
            await ctx.send("No song is playing")  # if nothing is playing

    @commands.command(aliases=["skip"])  # to ensure that !skip command is also used for the same purpose
    async def stop(self, ctx):  # stop method
        if ctx.voice_client.is_playing() == True:
            ctx.voice_client.stop()
        else:
            await ctx.send("No song is  on the queue")  # if nothing is playing

    @commands.command()
    async def resume(self, ctx):  # resume method
        if ctx.voice_client.is_playing() == True:
            await ctx.send("Song is playing...")
        else:
            ctx.voice_client.resume()

    @commands.command()  # method to show the users the queue
    async def showlist(self, ctx):
        await ctx.send(f"Songs to be played: ** {str(self.song_queue)} ** ")


def setup(client):
    client.add_cog(Music(client))
