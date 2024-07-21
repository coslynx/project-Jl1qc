import ffmpeg
import requests
import asyncio
from config import config

# Global variables for music playback
queue = []
current_song = None
voice_client = None
volume = 0.5

# Function to download a song from a given URL using FFmpeg
def download_song(song_url):
    """Downloads a song from a given URL using FFmpeg.

    Args:
        song_url: The URL of the song to download.

    Returns:
        The path to the downloaded song file.
    """
    try:
        # Use FFmpeg to download the song
        download_path = f"{config['DOWNLOAD_PATH']}/{song_url.split('/')[-1]}.mp3"
        ffmpeg.download(song_url, download_path)
        return download_path
    except Exception as e:
        print(f"Error downloading song: {e}")
        return None

# Function to retrieve information about a song from the YouTube Music API
async def get_song_info(song_url):
    """Retrieves information about a song from the YouTube Music API.

    Args:
        song_url: The URL of the song.

    Returns:
        A dictionary containing the song's title, artist, album, and other relevant information.
    """
    try:
        # Make a request to the YouTube Music API to retrieve song information
        headers = {
            "Authorization": f"Bearer {config['YOUTUBE_API_KEY']}"
        }
        response = requests.get(
            f"https://youtube.googleapis.com/youtube/v3/videos?id={song_url}&part=snippet&key={config['YOUTUBE_API_KEY']}",
            headers=headers
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return {
            "title": data["items"][0]["snippet"]["title"],
            "artist": data["items"][0]["snippet"]["channelTitle"],
            "album": None,  # Not available from YouTube Music API
            "duration": None,  # Not available from YouTube Music API
        }
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving song information: {e}")
        return None

# Function to play a song using FFmpeg
async def play_song(ctx, voice_client, song_url):
    """Plays a song using FFmpeg.

    Args:
        ctx: The Discord context object.
        voice_client: The Discord voice client object.
        song_url: The URL of the song to play.
    """
    try:
        # Download the song using FFmpeg
        song_path = download_song(song_url)
        if song_path:
            # Create a FFmpeg audio source
            source = ffmpeg.input(song_path)
            source = ffmpeg.output(source, "pipe:", format="s16le", acodec="pcm_s16le", ac=2, ar="48000")
            source = ffmpeg.run_async(source)
            
            # Play the song
            voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source.pipe()), volume=volume))
            # Get song information from YouTube Music API
            song_info = await get_song_info(song_url)
            if song_info:
                await ctx.send(f"Now playing: {song_info['title']} by {song_info['artist']}")
            else:
                await ctx.send(f"Now playing: {song_url}")
    except Exception as e:
        print(f"Error playing song: {e}")
        await ctx.send(f"An error occurred while playing the song.")

# Function to get the current queue of songs
def get_queue():
    """Gets the current queue of songs.

    Returns:
        A list of dictionaries containing the song information (title, URL, etc.).
    """
    return queue

# Function to clear the current queue of songs
def clear_queue():
    """Clears the current queue of songs."""
    global queue
    queue.clear()

# Function to shuffle the current queue of songs
def shuffle_queue():
    """Shuffles the current queue of songs."""
    global queue
    import random
    random.shuffle(queue)

# Function to set the playback volume
def set_volume(volume):
    """Sets the playback volume.

    Args:
        volume: The new volume level (between 0 and 1).
    """
    global voice_client
    voice_client.source.volume = volume