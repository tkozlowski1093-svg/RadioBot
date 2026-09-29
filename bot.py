import discord
from discord.ext import commands

# Konfiguracja uprawnień bota
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Twój długi link z chunklist skopiowany z przeglądarki
STREAM_URL = "https://stream-cdn-1.open.fm/OFM57/ngrp:standard/chunklist_b192000.m3u8?t=8753cd975da246e2f62d0dbd9e413a32db43ef3abbf3f3a9d5c6e2fbf843d0d2c510fe754259e227f80af1227dd911c23959d1f9d48733b62cd12400e2c17abcbc2b14231ffbd6061d5b396d014f3077d34b63ebafa17112b7a8f13d45d3f02993ab3263ba498676d9a528f8b36a0bb67e916987b5c2a7a57fa08d8c11458d45d0f06e29be9d30667b0cd02e0705dc90b0c5e046792cceba0191f09e63cb876da86b24dcaf2c660226acf2114a08e6d75ef3c8df0a091acd262114bd28f2d4886ba57be054cff7d29662c734e567b1c50bd30af7faef7eb20986b52f6ab6d5953e0311c1a8165cfc1e989e59084326" 

# Specjalne parametry dla strumieni HLS (Open FM)
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -fflags nobuffer', 
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f'Zalogowano pomyślnie jako {bot.user}, Mości Panie!')

@bot.command()
async def graj(ctx):
    if not ctx.author.voice:
        await ctx.send("Musisz być na kanale głosowym, abym mógł dołączyć!")
        return

    channel = ctx.author.voice.channel
    
    try:
        voice_client = await channel.connect()
    except discord.ClientException:
        voice_client = ctx.voice_client

    if not voice_client.is_playing():
        # Używamy pobranego pliku ffmpeg.exe z tego samego folderu
        source = discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=STREAM_URL, **FFMPEG_OPTIONS)
        voice_client.play(source)
        await ctx.send(f"Rozpoczynam transmisję na kanale {channel.name}.")
    else:
        await ctx.send("Radio już gra na tym kanale!")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Zatrzymano odtwarzanie i rozłączono.")

# Podmień poniższy tekst na swój token z notatnika
import os
TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)