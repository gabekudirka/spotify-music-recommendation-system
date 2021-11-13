import json
import os

from collections import namedtuple

class Playlist:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Track:
    def __init__(self, **entries):
        self.__dict__.update(entries)

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

            for track in current_dict_playlist['tracks']:
                current_track = Track(**track)
                current_playlist_tracks.append(current_track)

            current_dict_playlist['tracks'] = current_playlist_tracks

            new_playlist = Playlist(**current_dict_playlist)
            self.playlists.append(new_playlist)

if __name__ == '__main__':
    p = PlaylistDecoder()
    p.decode()
    print(p.playlists[0].tracks[0].__dict__)
