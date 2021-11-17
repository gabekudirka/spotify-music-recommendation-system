import json
import math
import os
import spotipy

from itertools import islice
from playlist_decoder import PlaylistDecoder
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy_helper import SpotipyHelper

class SongAttributeEncoder:

    playlist_directory = r'spotify_million_playlist_dataset/data'

    def __init__(self):
        self.helper = SpotipyHelper()
        self.tracks = set()

    def decode_playlist_files_to_tracks(self):
        playlist_filenames = os.listdir(PlaylistDecoder.playlist_directory)[:1]

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

            for track in current_dict_playlist['tracks']:
                self.tracks.add(track['track_uri'])

        f.close()

    def __batch(self, iterable, n=1):
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx:min(ndx + n, l)]

    def create_track_attribute_files(self):
        assert not os.path.exists(os.path.join(os.getcwd(), 'spotify_track_attributes')), 'path "spotify_track_attributes" already exists'

        # Create directory for holding attribute files
        os.mkdir('spotify_track_attributes')

        # 1000 songs per file
        batched_tracks_file = self.__batch(list(self.tracks), n = 1000)

        current_file_index = 0

        ### Notify how many expected files
        print(f'{len(self.tracks)} total tracks, expecting { math.ceil(len(self.tracks) / 1000) } json files')
        ###

        for batch_index, batch_file in enumerate(batched_tracks_file):

            ### Notify about current batch progress
            print(f'- Currently creating batch { batch_index }               ', end='\r')
            ###

            current_file_track_attributes = {}

            batched_track_attributes = self.__batch(list(batch_file), n = 100)

            # get 100 tracks at a time
            for track_batch_index, track_attribute_batch in enumerate(batched_track_attributes):

                # array of attributes, positionally respective to input track_ids
                spotify_return_attributes = self.helper.get_attributes_for_track_batch(track_attribute_batch)

                for index, track_id in enumerate(track_attribute_batch):
                    current_file_track_attributes[track_id] = spotify_return_attributes[index]

            with open(f'spotify_track_attributes/song-attributes-{ current_file_index }.json', 'w') as f:
                json.dump({'songs': current_file_track_attributes}, f, ensure_ascii=False, indent=4)

            current_file_index += 1


if __name__ == '__main__':
    print("Decoding Playlist files and retrieving Spotify track attributes")
    print("----------")
    encoder = SongAttributeEncoder()
    encoder.decode_playlist_files_to_tracks()
    encoder.create_track_attribute_files()
