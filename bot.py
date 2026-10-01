import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Zalogowano pomyślnie jako {bot.user}, Mości Panie!')

@bot.command()
async def graj(ctx):
    if not ctx.author.voice:
        await ctx.send("Musisz być na kanale głosowym, abym mógł dołączyć!")
        return
        
    channel = ctx.author.voice.channel
    
    if not ctx.voice_client:
        voice_client = await channel.connect()
    else:
        voice_client = ctx.voice_client

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    
    # Stały, bezpośredni link do strumienia MP3 Open FM (np. stacja Impreza)
    url_radia = "http://s4.radioparty.pl:8000/"
    if not voice_client.is_playing():
        source = discord.FFmpegPCMAudio(url_radia, **FFMPEG_OPTIONS)
        voice_client.play(source)
        await ctx.send("📻 Odtwarzam Radio Party GEJUCHYY!")
    else:
        await ctx.send("Już coś gram!")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Wyszedłem z kanału. Cisza w eterze!")
    else:
        await ctx.send("Nie ma mnie na żadnym kanale!")

TOKEN = os.environ.get("DISCORD_TOKEN") 

if TOKEN:
    bot.run(TOKEN)
else:
    print("BŁĄD: Nie znaleziono zmiennej DISCORD_TOKEN!")
