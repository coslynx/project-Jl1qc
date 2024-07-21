import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from config import config
from utils.music_utils import *

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix=config['PREFIX'], intents=intents)

@bot.event
async def on_ready():
    print(f'MelodyBot is online as {bot.user}')

@bot.command(name='play', help='Plays a song from YouTube Music.')
async def play(ctx, *, search):
    try:
        voice_client = await join_voice_channel(ctx)
        if voice_client:
            song_url = await get_song_url(search)
            if song_url:
                await play_music(ctx, voice_client, song_url)
            else:
                await ctx.send("No song found. Please try a different search term.")
        else:
            await ctx.send("Please join a voice channel first.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name='pause', help='Pauses the currently playing song.')
async def pause(ctx):
    try:
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.pause()
            await ctx.send("Paused.")
        else:
            await ctx.send("Nothing is playing.")
    except AttributeError:
        await ctx.send("Bot is not connected to a voice channel.")

@bot.command(name='resume', help='Resumes the currently paused song.')
async def resume(ctx):
    try:
        voice_client = ctx.voice_client
        if voice_client.is_paused():
            voice_client.resume()
            await ctx.send("Resumed.")
        else:
            await ctx.send("Nothing is paused.")
    except AttributeError:
        await ctx.send("Bot is not connected to a voice channel.")

@bot.command(name='skip', help='Skips the current song and plays the next one.')
async def skip(ctx):
    try:
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Skipped.")
        else:
            await ctx.send("Nothing is playing.")
    except AttributeError:
        await ctx.send("Bot is not connected to a voice channel.")

@bot.command(name='stop', help='Stops the music and disconnects from the voice channel.')
async def stop(ctx):
    try:
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send("Stopped and disconnected.")
    except AttributeError:
        await ctx.send("Bot is not connected to a voice channel.")

@bot.command(name='queue', help='Shows the current queue of songs.')
async def queue(ctx):
    try:
        queue_list = get_queue()
        if queue_list:
            queue_string = "\n".join(f"{i+1}. {song['title']}" for i, song in enumerate(queue_list))
            await ctx.send(f"Current Queue:\n{queue_string}")
        else:
            await ctx.send("The queue is empty.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name='clear', help='Clears the current queue of songs.')
async def clear(ctx):
    try:
        clear_queue()
        await ctx.send("Queue cleared.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name='shuffle', help='Shuffles the current queue of songs.')
async def shuffle(ctx):
    try:
        shuffle_queue()
        await ctx.send("Queue shuffled.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name='volume', help='Sets the playback volume.')
async def volume(ctx, volume: int):
    try:
        if 0 <= volume <= 100:
            set_volume(volume / 100)
            await ctx.send(f"Volume set to {volume}%")
        else:
            await ctx.send("Volume must be between 0 and 100.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

async def join_voice_channel(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        try:
            voice_client = await channel.connect()
            return voice_client
        except discord.errors.ClientException:
            await ctx.send("The bot is already in a voice channel.")
            return None
    else:
        await ctx.send("You are not connected to a voice channel.")
        return None

bot.run(os.getenv('DISCORD_TOKEN'))