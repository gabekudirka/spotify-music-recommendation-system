import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")