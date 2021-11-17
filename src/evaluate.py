from objects.cluster import TrackClusterer
from objects.playlist_decoder import PlaylistDecoder
from objects.spotify_song_attribute_decoder import TrackAttributeDecoder


if __name__ == '__main__':

    ###
    ### Mark - Decode all data
    ###

    # Decode playlists
    playlist_decoder = PlaylistDecoder()
    playlist_decoder.decode()

    # Decode track attributes
    track_attributes_decoder = TrackAttributeDecoder()
    track_attributes_decoder.decode_attribute_files()

    ###
    ### Mark - Cluster
    ###

    # Cluster tracks
    track_clusterer = TrackClusterer(playlist_decoder.playlists[0].tracks, playlist_decoder.playlists[1].tracks[0])
    track_clusterer.cluster()
