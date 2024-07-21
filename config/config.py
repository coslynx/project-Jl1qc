import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "DISCORD_TOKEN": os.getenv("DISCORD_TOKEN"),
    "YOUTUBE_API_KEY": os.getenv("YOUTUBE_API_KEY"),
    "DATABASE_PATH": os.getenv("DATABASE_PATH"),
    "PREFIX": os.getenv("PREFIX"),
    "DOWNLOAD_PATH": os.getenv("DOWNLOAD_PATH"),
}