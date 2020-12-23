import discord
import random
from discord.ext import commands
from bs4 import BeautifulSoup
import urllib
import youtube_dl
import os

app = commands.Bot(command_prefix = '!')
app.remove_command('help')

@app.event
async def on_ready():
    print('다음으로 로그인합니다:')
    print(app.user.name)
    print('connection was successful')
    print('----------')
    await app.change_presence(activity = discord.Game(name='개발'))

@app.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = 'General')
    await voiceChannel.connect()
    voice = discord.utils.get(app.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@app.command()
async def leave(ctx):
    voice = discord.utils.get(app.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@app.command()
async def pause(ctx):
    voice = discord.utils.get(app.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@app.command()
async def resume(ctx):
    voice = discord.utils.get(app.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@app.command()
async def stop(ctx):
    voice = discord.utils.get(app.voice_clients, guild=ctx.guild)
    voice.stop()

@app.command()
async def devnote(ctx):
    embed = discord.Embed(title = '개발노트' , color = 0x008000)
    embed.add_field(name = "ver 1.0" , value = "Hello, World!" , inline = False)
    embed.add_field(name = "ver 1.1" , value = "유튜브 기반 음악 기능 추가" , inline = False)

    await ctx.send(embed = embed)


@app.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(title = 'Commend Help', description = 'Ver = 1.1' , color = 0xFF5733)
    embed.add_field(name = "!dice", value = "1~6범위 내의 난수를 알려줍니다" , inline = True)
    embed.add_field(name = "!repeat [반복할말]", value = "입력된 말을 SkyBlue가 다시 말합니다" , inline = False)
    embed.add_field(name = "!hello" , value = "Hello, World!" , inline = False)
    embed.add_field(name = "!play [유튜브 음악 URL]" , value = "입력받은 유튜브 URL의 영상을 오디오로 변환하며 재생합니다" , inline = False)
    embed.add_field(name = "!pause !resume !stop" , value = "각각 멈춤, 재생, 종료입니다" , inline = False)

    await ctx.send(embed = embed)

@app.command()
async def repeat(ctx,*,text):
    await ctx.send(text)    


@app.command()
async def dice(ctx):
    await ctx.send(random.randrange(1,7))



app.run('Token')  #github 푸시할때 토큰 가리세요      