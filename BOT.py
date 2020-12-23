import discord
import random
from discord.ext import commands
from bs4 import BeautifulSoup
import urllib
import youtube_dl
import os
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
import warnings
import requests
import time
import asyncio

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
async def corona(ctx):
    covidSite = "http://ncov.mohw.go.kr/index.jsp"
    html = urlopen(covidSite)
    bs = BeautifulSoup(html, 'html.parser')
    statisticalNumbers = bs.findAll('span', {'class': 'num'})
    beforedayNumbers = bs.findAll('span', {'class': 'before'})

    # 통계수치
    statNum = []
    # 전일대비 수치
    beforeNum = []
    for num in range(7):
        statNum.append(statisticalNumbers[num].text)
    for num in range(4):
        beforeNum.append(beforedayNumbers[num].text.split('(')[-1].split(')')[0])

    totalPeopletoInt = statNum[0].split(')')[-1].split(',')
    tpInt = ''.join(totalPeopletoInt)
    lethatRate = round((int(statNum[3]) / int(tpInt)) * 100, 2)
    embed = discord.Embed(title="Covid-19 Virus Korea Status", description="",color=0x5CD1E5)
    embed.add_field(name="Data source : Ministry of Health and Welfare of Korea", value="http://ncov.mohw.go.kr/index.jsp", inline=False)
    embed.add_field(name="확진환자(누적)", value=statNum[0].split(')')[-1]+"("+beforeNum[0]+")",inline=True)
    embed.add_field(name="완치환자(격리해제)", value=statNum[1] + "(" + beforeNum[1] + ")", inline=True)
    embed.add_field(name="치료중(격리 중)", value=statNum[2] + "(" + beforeNum[2] + ")", inline=True)
    embed.add_field(name="사망", value=statNum[3] + "(" + beforeNum[3] + ")", inline=True)
    embed.add_field(name="누적확진률", value=statNum[6], inline=True)
    embed.add_field(name="치사율", value=str(lethatRate) + " %",inline=True)

    await ctx.send(embed = embed)



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
    embed.add_field(name = "ver 1.2" , value = "코로나19 상황판, 룰렛 추가" , inline = False)

    await ctx.send(embed = embed)


@app.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(title = 'Commend Help', description = 'Ver = 1.2' , color = 0xFF5733)
    embed.add_field(name = "!dice", value = "1~6범위 내의 난수를 알려줍니다" , inline = True)
    embed.add_field(name = "!repeat [반복할말]", value = "입력된 말을 SkyBlue가 다시 말합니다" , inline = False)
    embed.add_field(name = "!hello" , value = "Hello, World!" , inline = False)
    embed.add_field(name = "!play [유튜브 음악 URL]" , value = "입력받은 유튜브 URL의 영상을 오디오로 변환하며 재생합니다" , inline = False)
    embed.add_field(name = "!pause !resume !stop" , value = "각각 멈춤, 재생, 종료입니다" , inline = False)
    embed.add_field(name = "!corona" , value = "현재 코로나19 상황을 말해줍니다" , inline = False)
    embed.add_field(name = "!roulette [렌덤으로 한개 뽑을 목록]" , value = "띄어쓰기로 구분됩니다" , inline = False)

    await ctx.send(embed = embed)

@app.command()
async def repeat(ctx,*,text):
    await ctx.channel.purge(limit = 1)
    await ctx.send(text)    
    


@app.command()
async def dice(ctx):
    await ctx.send(random.randrange(1,7))

@app.command()
async def roulette(ctx,*list):
    await ctx.send('두구두구...')
    await asyncio.sleep(2)
    await ctx.send(random.choice(list))



app.run('Token')  #github 푸시할때 토큰 가리세요      