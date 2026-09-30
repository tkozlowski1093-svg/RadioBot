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
    url_radia = "https://stream-cdn-1.open.fm/OFM57/ngrp:standard/chunklist_b192000.m3u8?t=7aa9c60b66fbe1195b50928f622660bd02ea664f44fabb6e895a9f76d8b71bc1098a2a633f6e674894b99853d143ebc63de66226af5fff675120a3ec5b0c827d8d05acee8451dde9e816dbd93469a9015d4b2bdbe94d7dc3ada350af4f5b2277fe88198790a80b5474810aade63ca60750cdc5c8b792e379f4ad7b3e1eb207935145dea5d0f3cfe69dad4678fca615a3b8114a9110b45663b38a43aca491f4f2ebbe2658ad462ed5945607ac7b3d281db8b902322143165126963ee8496cc4247c720eb34c1e8e96856744269702be9a879109d93c060f5dfc645b4d133fbc233eac7333b0efd57f2cc7bcfcdb9c"
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
