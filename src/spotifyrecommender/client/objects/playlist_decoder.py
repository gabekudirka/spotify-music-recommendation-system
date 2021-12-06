import json
import os

class Playlist:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Track:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class PlaylistDecoder:

    playlist_directory = r'spotify_million_playlist_dataset/data'

    def __init__(self):
        self.playlists = []
        self.tracks = {}

    def decode(self):
        playlist_filenames = os.listdir(PlaylistDecoder.playlist_directory)

        # decode just first 10 playlists for testing
        playlist_filenames = playlist_filenames[:10]

        file_amount = len(playlist_filenames)
        print(f'{ file_amount } playlist files to decode')

        for index, filename in enumerate(playlist_filenames):
            print(f'- decoding playlist file { index + 1 }/{ file_amount }: { filename }          ', end='\r')
            self.decodeFile(filename)

        print(f'Done decoding { file_amount } playlist files                                        ')

    def decodeFile(self, filename):
        f = open(PlaylistDecoder.playlist_directory + "/" + filename)
        data = json.load(f)

        for i in range(0, len(data['playlists'])):

            current_dict_playlist = data['playlists'][i]
            current_playlist_tracks = []

            for track in current_dict_playlist['tracks']:
                current_track = Track(**track)
                self.tracks[current_track.track_uri] = current_track
                current_playlist_tracks.append(current_track.track_uri)

            current_dict_playlist['tracks'] = current_playlist_tracks

            new_playlist = Playlist(**current_dict_playlist)
            self.playlists.append(new_playlist)

if __name__ == '__main__':
    p = PlaylistDecoder()
    p.decode()
    print(len(p.tracks))
