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
    url_radia = "https://stream-cdn-1.open.fm/OFM57/ngrp:standard/playlist.m3u8?t=baf624f5369b4ac2aaa317fe913dc50a9714803dfd0f9e5ab047ff1dacdaa6ed8f09077079a2024b4882285f51d19f0aa7c87b993a5b4a87e2c40e72a188ef3aefd98a7c93ad50fc179d763d862c4a6c403264c38879b95c8affdb3ca0f12b33b9ee9753e0dd5127b897da1fafae40b0091ec975bbe2448ca9cf16b371a2f116599bb13c37b98b70b3ada5d662ab674ba2e262c2557cf4f14a02ee9b33fcbb00b2bd1d44395a3def5bb36d8baf561b33ecb41d2c4b4be590eff01e28df0a1d599a4c7dfcb09182c7e01286a5bb58581a696c072166eb5a799a4e2ba6e48ab81248c7670b25979164"
    if not voice_client.is_playing():
        source = discord.FFmpegPCMAudio(url_radia, **FFMPEG_OPTIONS)
        voice_client.play(source)
        await ctx.send("📻 Odtwarzam Open FM!")
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
