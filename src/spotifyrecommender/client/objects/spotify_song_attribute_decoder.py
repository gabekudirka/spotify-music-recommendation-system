import json
import math
import os
import spotipy

from .playlist_decoder import PlaylistDecoder
from .spotipy_helper import SpotipyHelper
from spotipy.oauth2 import SpotifyClientCredentials

class TrackAttributeDecoder:

    attributes_directory = r'src/spotify_track_attributes'

    def __init__(self):
        self.tracks = {}

    def decode_attribute_files(self, num_files = 'all'):
        assert os.path.exists(os.path.join(os.getcwd(), 'src/spotify_track_attributes')), 'path "spotify_track_attributes" doesn\' exist'

        if num_files == 'all':
            attribute_filenames = os.listdir(TrackAttributeDecoder.attributes_directory)
        else:
            attribute_filenames = os.listdir(TrackAttributeDecoder.attributes_directory)[:num_files]

        file_amount = len(attribute_filenames)

        print(f'{ file_amount } attribute files to decode')

        for index, filename in enumerate(attribute_filenames):
            print(f'- decoding attribute file { index + 1 }/{ file_amount }: { filename }          ', end='\r')
            self.decode_file(filename)

        no_attribute_tracks = list(filter(lambda track: self.tracks[track] is None , self.tracks))

        print(f'{len(no_attribute_tracks)} without attributes, normalizing them with default values                     ')

        # Arbitrarily chosen based upon looking at other values in the dataset
        default_attributes = { "danceability" : 0.4,
        "energy" : 0.4,
        "key" : 3,
        "loudness" : -2,
        "mode" : 1,
        "speechiness" : 0.02,
        "acousticness" : 0.02,
        "instrumentalness" : 0.02,
        "liveness" : 0.02,
        "valence" : 0.02 ,
        "tempo" : 80}

        for no_attribute_track in no_attribute_tracks:
            self.tracks[no_attribute_track] = default_attributes

        print(f'Done decoding { file_amount } attribute files                                        ')

    def decode_file(self, filename):
        f = open(TrackAttributeDecoder.attributes_directory + "/" + filename)
        data = json.load(f)

        for track_uri in data['songs'].keys():
            self.tracks[track_uri] = data['songs'][track_uri]

if __name__ == '__main__':
    d = TrackAttributeDecoder()
    d.decode_attribute_files()

    print(d.tracks[:50])
