import json
import numpy as np
import pandas as pd
import sys

from predict import PredictSongs
from objects.spotify_song_attribute_decoder import TrackAttributeDecoder
from objects.spotipy_helper import SpotipyHelper

class ChallengeSetCreator():
    def __init__(self, submission_filename):
        self.t = TrackAttributeDecoder()
        self.t.decode_attribute_files()

        self.p = PredictSongs(self.t.tracks)
        self.playlist_predictions = []
        self.helper = SpotipyHelper()
        self.submission_filename = submission_filename

    def create_playlist_csv(self):
        # add team info

        f = open(self.submission_filename, "w")
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

        playlist_track_uris = [track['track_uri'] for track in playlist['tracks']][:1]

        track_attributes = []

        for track_uri in playlist_track_uris:
            attributes = self.t.tracks[track_uri]

            track_attributes.append(attributes)

        final_form = {}
        for index, track_id in enumerate(playlist_track_uris):
            final_form[track_id] = track_attributes[index]

        return final_form

    def create_challenge_set(self):
        f = open('challenge_set.json')
        data = json.load(f)

        challenge_playlists = data['playlists'][3000:4000]

        playlists_with_attributes = []

        for playlist in challenge_playlists:
            playlists_with_attributes.append(self.get_attributes_for_tracks_in_playlist(playlist))

        for i, attributed_playlist in enumerate(playlists_with_attributes):
            self.predict_tracks_for_playlist(challenge_playlists[i], attributed_playlist)

        self.create_playlist_csv()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: python create_challenge_set.py submission.csv")
        sys.exit()

    submission_filename = sys.argv[1]

    c = ChallengeSetCreator(submission_filename)
    c.create_challenge_set()
