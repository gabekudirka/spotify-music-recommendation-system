from objects.spotify_song_attribute_decoder import TrackAttributeDecoder
import numpy

class TopSongs:

    def mse(song, target):
        totalDif = 0
        attributes = [ "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
        for attribute in attributes:
            totalDif += (target[attribute] - song[attribute ])**2
        return totalDif

    def getSimilarSongs(songs, target, n):
        topSongs = {}
        for key, val in songs.items():
            score = TopSongs.mse(val,target)
            topSongs[key]=score
        sortedSongs = {k: v for k, v in sorted(topSongs.items(), key=lambda item: item[1])}
        #print(sortedSongs)
        return list(sortedSongs.items())[:n]


        

if __name__ == '__main__':
    d = TrackAttributeDecoder()
    d.decode_attribute_files()
    #print(d.tracks.keys())
    print(TopSongs.getSimilarSongs(d.tracks,d.tracks["spotify:track:3G8eHnIYQX6Gbjc5vulISf"],5))