import json
import math
import os
import spotipy

from itertools import islice
from .playlist_decoder import PlaylistDecoder
from spotipy.oauth2 import SpotifyClientCredentials
from .spotipy_helper import SpotipyHelper

class TrackAttributeDecoder:

    attributes_directory = r'spotify_track_attributes'

    def __init__(self):
        self.tracks = {}

    def decode_attribute_files(self):
        assert os.path.exists(os.path.join(os.getcwd(), 'spotify_track_attributes')), 'path "spotify_track_attributes" doesn\' exist'

        attribute_filenames = os.listdir(TrackAttributeDecoder.attributes_directory)

        file_amount = len(attribute_filenames)
        print(f'{ file_amount } attribute files to decode')

        for index, filename in enumerate(attribute_filenames):
            print(f'- decoding attribute file { index + 1 }/{ file_amount }: { filename }          ', end='\r')
            self.decode_file(filename)

        print(f'Done decoding { file_amount } attribute files                                        ')

    def decode_file(self, filename):
        f = open(TrackAttributeDecoder.attributes_directory + "/" + filename)
        data = json.load(f)

        for track_uri in data['songs'].keys():
            self.tracks[track_uri] = data['songs'][track_uri]

        f.close()

if __name__ == '__main__':
    d = TrackAttributeDecoder()
    d.decode_attribute_files()
    print(d.tracks.keys())
