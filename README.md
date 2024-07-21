# MelodyBot: Your Discord Music Companion

## Introduction

MelodyBot is a Discord bot designed to bring the joy of music to your server. It offers a comprehensive suite of features, allowing you to play, control, and share music with your friends and community.

## Features

* **Music Playback:**
    * Play, pause, and skip songs.
    * Support for various audio formats (MP3, WAV, etc.).
    * Create and manage queues for continuous playback.
    * Shuffle the queue for a randomized listening experience.
    * View information about the currently playing song.
* **Search and Selection:**
    * Search for songs by title, artist, or keyword.
    * Browse search results with song details.
    * Select specific songs from search results.
* **Voice Channel Integration:**
    * Join and leave voice channels on command.
    * Control music playback from text channels.
    * Manage user permissions for music control.
* **User Interface:**
    * Simple and intuitive command system.
    * Help command for command usage instructions.
    * Customizable commands and aliases.
* **Additional Features:**
    * Volume control for adjusting playback levels.
    * Integration with popular music streaming services like YouTube Music.
    * Create and manage custom playlists.
    * Real-time lyrics display for a more immersive experience.

## Installation

1. **Install Python:** Ensure you have Python installed on your system ([https://www.python.org/](https://www.python.org/)).
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Create a `.env` file:**
   ```bash
   cp .env.example .env
   ```
   Replace placeholders in `.env` with your Discord Bot Token, YouTube Music API Key, and database path.
5. **Run the bot:**
   ```bash
   python main.py
   ```

## Usage

To use MelodyBot, simply type the bot's command prefix followed by a command.  The default prefix is `!`. For example:

* **Play a song:** `!play <song name or URL>`
* **Pause music:** `!pause`
* **Resume music:** `!resume`
* **Skip to the next song:** `!skip`
* **Stop music and leave voice channel:** `!stop`
* **View the current queue:** `!queue`
* **Clear the current queue:** `!clear`
* **Shuffle the queue:** `!shuffle`
* **Set the volume:** `!volume <volume level>`
* **Get help:** `!help`

**Note:**  You can customize the command prefix using the `!setprefix` command.

## Contributing

Contributions to MelodyBot are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## License

MelodyBot is released under the [MIT License](LICENSE).

## Disclaimer

This project is for educational purposes and is not affiliated with Discord or YouTube Music.