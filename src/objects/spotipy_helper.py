import os
import spotipy

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

class SpotipyHelper:
    def __init__(self):
        load_dotenv()

        SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
        SPOTIPY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")

        auth_manager = SpotifyClientCredentials(client_id = SPOTIPY_CLIENT_ID,
                                                client_secret = SPOTIPY_CLIENT_SECRET)
        self.client = spotipy.Spotify(auth_manager = auth_manager)

    def get_track_name(self, track_id):
        return self.client.track(track_id)["name"]

    def get_attributes_for_track(self, track_id):
        return self.client.audio_features(track_id)

    def get_attributes_for_track_batch(self, track_ids):
        assert len(track_ids) > 0, "Must call with at least one track id"
        assert len(track_ids) < 101, "Can only call with a maximum of 100 track ids"

        return self.client.audio_features(track_ids)


    