import discord
import random
from discord.ext import commands

app = commands.Bot(command_prefix = '!')
app.remove_command('help')

@app.event
async def on_ready():
    print('다음으로 로그인합니다:')
    print(app.user.name)
    print('connection was successful')
    await app.change_presence(activity = discord.Game(name='개발'))

@app.command()
async def hello(ctx):
    await ctx.send('Hello, World!')

@app.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(title = 'Help', description = 'Ver = 1.0' , color = 0xFF5733)
    embed.add_field(name = "!dice", value = "1~6범위 내의 난수를 알려줍니다" , inline = False)
    embed.add_field(name = "!repeat (반복할말)", value = "입력된 말을 SkyBlue가 다시 말합니다" , inline = False)
    embed.add_field(name = "!hello" , value = "Hello, World!" , inline = False)

    await ctx.send(embed = embed)

@app.command()
async def repeat(ctx,*,text):
    await ctx.send(text)    


@app.command()
async def dice(ctx):
    await ctx.send(random.randrange(1,7))



app.run('NzkwNDQ5OTUwMTY1MTcyMjQ0.X-Ax4Q.u9wS5E1ySquiAG2zdKMg-7AMBrA')                        