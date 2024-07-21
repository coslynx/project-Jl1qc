import discord
from discord.ext import commands
import asyncio
import ffmpeg
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize variables
queue = []
current_song = None
voice_client = None
volume = 0.5

class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play", help="Plays a song from YouTube Music.")
    async def play(self, ctx, *, search):
        global voice_client, current_song
        try:
            # Join voice channel
            voice_client = await join_voice_channel(ctx)
            if voice_client:
                # Search for song
                song_url = await get_song_url(search)
                if song_url:
                    # Add song to queue and play
                    await add_to_queue(ctx, song_url)
                    if not current_song:
                        await play_music(ctx, voice_client)
                else:
                    await ctx.send("No song found. Please try a different search term.")
            else:
                await ctx.send("Please join a voice channel first.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="pause", help="Pauses the currently playing song.")
    async def pause(self, ctx):
        global voice_client
        try:
            if voice_client.is_playing():
                voice_client.pause()
                await ctx.send("Paused.")
            else:
                await ctx.send("Nothing is playing.")
        except AttributeError:
            await ctx.send("Bot is not connected to a voice channel.")

    @commands.command(name="resume", help="Resumes the currently paused song.")
    async def resume(self, ctx):
        global voice_client
        try:
            if voice_client.is_paused():
                voice_client.resume()
                await ctx.send("Resumed.")
            else:
                await ctx.send("Nothing is paused.")
        except AttributeError:
            await ctx.send("Bot is not connected to a voice channel.")

    @commands.command(name="skip", help="Skips the current song and plays the next song in the queue.")
    async def skip(self, ctx):
        global voice_client, current_song
        try:
            if voice_client.is_playing():
                voice_client.stop()
                await ctx.send("Skipped.")
                # Play next song
                if queue:
                    current_song = queue.pop(0)
                    await play_music(ctx, voice_client)
        except AttributeError:
            await ctx.send("Bot is not connected to a voice channel.")

    @commands.command(name="stop", help="Stops the music playback and leaves the voice channel.")
    async def stop(self, ctx):
        global voice_client
        try:
            if voice_client.is_playing():
                voice_client.stop()
            await voice_client.disconnect()
            await ctx.send("Stopped and disconnected.")
        except AttributeError:
            await ctx.send("Bot is not connected to a voice channel.")

    @commands.command(name="queue", help="Shows the current queue of songs.")
    async def queue(self, ctx):
        global queue
        try:
            if queue:
                queue_string = "\n".join(f"{i+1}. {song['title']}" for i, song in enumerate(queue))
                await ctx.send(f"Current Queue:\n{queue_string}")
            else:
                await ctx.send("The queue is empty.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="clear", help="Clears the current queue of songs.")
    async def clear(self, ctx):
        global queue
        try:
            queue.clear()
            await ctx.send("Queue cleared.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="shuffle", help="Shuffles the current queue of songs.")
    async def shuffle(self, ctx):
        global queue
        try:
            import random
            random.shuffle(queue)
            await ctx.send("Queue shuffled.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="volume", help="Sets the playback volume.")
    async def volume(self, ctx, volume: int):
        global voice_client
        try:
            if 0 <= volume <= 100:
                set_volume(volume / 100)
                await ctx.send(f"Volume set to {volume}%")
            else:
                await ctx.send("Volume must be between 0 and 100.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def join_voice_channel(ctx):
    global voice_client
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

async def get_song_url(search):
    # Function to search for song URL using YouTube Music API
    # Replace with your actual YouTube Music API integration
    return search

async def add_to_queue(ctx, song_url):
    global queue, current_song
    # Function to add song to queue
    # Replace with your actual song information retrieval and storage
    song_title = song_url  # Replace with actual song title retrieval
    queue.append({"title": song_title, "url": song_url})
    await ctx.send(f"Added {song_title} to the queue.")

async def play_music(ctx, voice_client):
    global queue, current_song
    try:
        if queue:
            current_song = queue.pop(0)
            # Function to download song and play
            # Replace with your actual audio download and playback implementation
            await ctx.send(f"Now playing: {current_song['title']}")
            # Play music here
        else:
            await ctx.send("The queue is empty.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

def set_volume(volume):
    global voice_client
    voice_client.source.volume = volume

def setup(bot):
    bot.add_cog(MusicPlayer(bot))