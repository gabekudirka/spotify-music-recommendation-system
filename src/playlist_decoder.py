import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from test import extractSpotipyData

class Playlist:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Track:
    def __init__(self, track_features, audio_features):
        self.track_features = track_features
        self.audio_features = audio_features

class PlaylistDecoder():

    playlist_directory = r'spotify_million_playlist_dataset/data'

    def __init__(self):
        self.playlists = []

    def decode(self):
        playlist_filenames = []

        for filename in os.listdir(PlaylistDecoder.playlist_directory):
            playlist_filenames.append(filename)

        # decode just first playlist for testing
        playlist_filenames = sorted(playlist_filenames)
        self.decodeFile(playlist_filenames[0])

        # for filename in playlist_filenames:
            # decodeFile(filename)

    def decodeFile(self, filename):
        f = open(PlaylistDecoder.playlist_directory + "/" + filename)
        data = json.load(f)

        for i in range(0, len(data['playlists'])):
            current_dict_playlist = data['playlists'][i]
            current_playlist_tracks = []
            
            current_playlist_track_uris = [track['track_uri'] for track in current_dict_playlist['tracks']]
            current_playlist_track_features = self.extractTrackData(current_dict_playlist['tracks'], current_playlist_track_uris)

            for track_features in current_playlist_track_features:
                #spotipy_features = self.extractTrackData(track['track_uri'])
                #track_features = dict(track, **spotipy_features)
                current_track = Track(track_features[0], track_features[1])
                current_playlist_tracks.append(current_track)

            current_dict_playlist['tracks'] = current_playlist_tracks

            new_playlist = Playlist(**current_dict_playlist)
            self.playlists.append(new_playlist)

    def extractTrackData(self, tracks, track_ids):
        client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        used_audio_feature_names = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
                            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
        used_track_feature_names = ['artist_name', 'track_name', 'album_name']
        
        # track_analysis = sp.audio_analysis(track_ida)

        # You can only get data on 100 tracks at a time
        all_audio_features_arr = self.divide_playlist(track_ids, 100)
        playlist_audio_features = []
        playlist_track_features = []
        i = 0
        for features_chunk in all_audio_features_arr:
            all_audio_features = sp.audio_features(features_chunk)

            for audio_feature in enumerate(all_audio_features):
                used_audio_features = {x:audio_feature[1][x] for x in used_audio_feature_names}
                used_track_features = {x:tracks[i][x] for x in used_track_feature_names}
                playlist_audio_features.append(used_audio_features)
                playlist_track_features.append(used_track_features)
                i += 1
        


        return zip(playlist_track_features, playlist_audio_features)

    def divide_playlist(self, l, n):
        for i in range(0, len(l), n): 
            yield l[i:i + n]


if __name__ == '__main__':
    p = PlaylistDecoder()
    p.decode()
    print(p.playlists[0].tracks[0].__dict__)
