import json
import numpy as np
import pandas as pd

from predict import PredictSongs
from objects.spotify_song_attribute_decoder import TrackAttributeDecoder
from objects.spotipy_helper import SpotipyHelper

class ChallengeSetCreator():
    def __init__(self):
        t = TrackAttributeDecoder()
        t.decode_attribute_files()

        self.p = PredictSongs(t.tracks)
        self.playlist_predictions = []
        self.helper = SpotipyHelper()

    def create_playlist_csv(self):
        # add team info

        f = open("submission.csv", "w")
        f.write('team_info,InformationRetrievalFall2021Pippin,ethanpippin2343@gmail.com\n')

        for prediction in self.playlist_predictions:
            f.write(','.join(prediction))
            f.write('\n')

        f.close()

    def predict_tracks_for_playlist(self, playlist, final_form):

        pid = playlist['pid']

        predicted_tracks = self.p.predict(final_form, 500)

        final = [f'{pid}'] + predicted_tracks

        self.playlist_predictions.append(final)

    def get_attributes_for_tracks_in_playlist(self, playlist):

        playlist_track_uris = [track['track_uri'] for track in playlist['tracks']]

        track_attributes = self.helper.get_attributes_for_track_batch(playlist_track_uris)

        final_form = {}
        for index, track_id in enumerate(playlist_track_uris):
            final_form[track_id] = track_attributes[index]

        return final_form

    def create_challenge_set(self):
        f = open('challenge_set.json')
        data = json.load(f)

        challenge_playlists = data['playlists']

        # do this first so that session stays alive with Spotify
        playlists_with_attributes = []

        for playlist in challenge_playlists:
            playlists_with_attributes.append(self.get_attributes_for_tracks_in_playlist(playlist))

        for i, attributed_playlist in enumerate(playlists_with_attributes):
            self.predict_tracks_for_playlist(challenge_playlists[i], attributed_playlist)

        self.create_playlist_csv()


if __name__ == '__main__':
    c = ChallengeSetCreator()
    c.create_challenge_set()
