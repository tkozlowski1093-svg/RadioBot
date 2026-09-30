import discord
from discord.ext import commands
import os

try:
    import nacl
    print(">>> PyNaCl jest poprawnie załadowany w systemie!")
except ImportError:
    print(">>> UWAGA: PyNaCl NIE JEST widoczny dla Pythona!")
    
# Konfiguracja uprawnień bota
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Link do strumienia HLS (Open FM)
STREAM_URL = "https://stream-cdn-1.open.fm/OFM57/ngrp:standard/chunklist_b192000.m3u8?t=11dc0c46b397f06babe6bf83c771d0548e0ad5bd46323e6cf9da170999706ce9238b7bdb302845c36aa741385425c45f06a3505ce4f33eb1f768e114e676d856bd6afa9843d0909fbee081cbbbf4c561cdeea3ae3b54a55d4a82d5e9cd25aa691aa6ae67c7209883b6928028c090efb8e1263584512ed5dba1f8d67b38009136dab4d25d6da033e39c2bb54042df6615acdf9d429d074e10783a3bc07377181042a66b7043a1cb394425e5aaf048e2c09a528ffe52c327619e686dab8526fb706e0d324464af47d8e492909a883981071179ecb4cf97bfaec4c0987fc35e633bb39742271e10f0ede4ea1a4eed5a1bff0626b24d56526dbbfff52f"
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
    
    if ctx.voice_client is None:
        voice_client = await channel.connect()
    else:
        voice_client = ctx.voice_client
        await voice_client.move_to(channel)

    if not voice_client.is_playing():
        source = discord.FFmpegPCMAudio(STREAM_URL, **FFMPEG_OPTIONS)
        voice_client.play(source)
        await ctx.send(f"Rozpoczynam transmisję na kanale {channel.name}.")
    else:
        await ctx.send("Radio już gra na tym kanale!")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Zatrzymano odtwarzanie i rozłączono.")
    else:
        await ctx.send("Nie jestem na żadnym kanale.")

TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)

# refresh
