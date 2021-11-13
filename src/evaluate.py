from playlist_decoder import PlaylistDecoder
from cluster import TrackClusterer

if __name__ == '__main__':

    # Decode playlists
    playlist_decoder = PlaylistDecoder()
    playlist_decoder.decode()

    # Cluster tracks
    track_clusterer = TrackClusterer(playlist_decoder.playlists[0].tracks, playlist_decoder.playlists[1].tracks[0])
    track_clusterer.cluster()
