import discord
from discord.ext import commands
import os

# Konfiguracja intencji (niezbędne, aby bot czytał komendy na czacie)
intents = discord.Intents.default()
intents.message_content = True

# Inicjalizacja bota z prefiksem "!"
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Zalogowano pomyślnie jako {bot.user}, Mości Panie!')

@bot.command()
async def graj(ctx):
    # Sprawdzenie czy użytkownik jest na kanale głosowym
    if not ctx.author.voice:
        await ctx.send("Musisz być na kanale głosowym, abym mógł dołączyć!")
        return
        
    channel = ctx.author.voice.channel
    
    # Dołączanie do kanału (lub pobranie obecnego połączenia)
    if not ctx.voice_client:
        voice_client = await channel.connect()
    else:
        voice_client = ctx.voice_client

    # Parametry FFmpeg wymuszające ciągłe odtwarzanie bez zrywania
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    
    # Twój link źródłowy z Open FM (.m3u8)
    url_radia = "https://stream-cdn-1.open.fm/OFM57/ngrp:standard/chunklist_b192000.m3u8?t=830e79b2df44863f5f96d797c3851bea03697070faf1949d40630165aec45230b57981714c764b512de80c4919adc061e83509c3f606b548f2e5a6f3471ef2c74018f9811461cebe00f4d0c144b23d25ab81b374ee09439dfc1526a197055e3ad8bd599c281144861a445d3b66ee9a274bfabddfdf6df915021bcc4299133936af56200d8aa7173358fafb5c076a31caad24f4e1e3d77aab5f0cb6b62bd51c06b4e5fef6e0d099e6232c640397d7769733e7727dafbb03d24e7584c4ee4b7de5d723d71b62334c71a24582a8cd03f8d5c3fc9f3d614c5e302f37893345910f2562c1cd4c2bbbda0c08dfc1fb8ca5f67d2d31688a8dbdf30fa991f9b6"

    # Uruchomienie strumienia audio
    if not voice_client.is_playing():
        source = discord.FFmpegPCMAudio(url_radia, **FFMPEG_OPTIONS)
        voice_client.play(source)
        await ctx.send("📻 Odtwarzam Open FM z Twojego linku!")
    else:
        await ctx.send("Już coś gram!")

@bot.command()
async def stop(ctx):
    # Wyjście z kanału i zatrzymanie radia
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Wyszedłem z kanału. Cisza w eterze!")
    else:
        await ctx.send("Nie ma mnie na żadnym kanale!")

# Pobieranie tokenu (skonfiguruj zmienną DISCORD_TOKEN w zakładce Variables na Railway)
TOKEN = os.environ.get("DISCORD_TOKEN") 

if TOKEN:
    bot.run(TOKEN)
else:
    print("BŁĄD: Nie znaleziono zmiennej DISCORD_TOKEN!")
