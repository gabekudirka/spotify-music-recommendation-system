from objects.spotify_song_attribute_decoder import TrackAttributeDecoder
import numpy

class TopSongs:
    def __init__(self):
        self.attributes = [ "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
        
    def normalizeAttr(self, songs):
        #print(numpy.zeros(len(self.attributes)))
        sums = dict(zip(self.attributes,numpy.zeros(len(self.attributes))))
        #print(sums)
        for key, vals in songs.items():
            for attribute in self.attributes:
                sums[attribute]+=vals[attribute]
        normSongs = songs
        for key, vals in songs.items():
            for attribute in self.attributes:
                normSongs[key][attribute] = vals[attribute]/sums[attribute]
        return normSongs

    def mse(self, song, target):
        totalDif = 0
        for attribute in self.attributes:
            totalDif += (target[attribute] - song[attribute ])**2
        return totalDif

    def getSimilarSongs(self, songs, target, n):
        self.normalizeAttr(songs)
        topSongs = {}
        for key, val in songs.items():
            score = self.mse(val,target)
            topSongs[key]=score
        sortedSongs = {k: v for k, v in sorted(topSongs.items(), key=lambda item: item[1])}
        #print(sortedSongs)
        return list(sortedSongs.items())[:n]


        

if __name__ == '__main__':
    d = TrackAttributeDecoder()
    d.decode_attribute_files()
    #print(d.tracks.keys())
    t =TopSongs()
    print(t.getSimilarSongs(d.tracks,d.tracks["spotify:track:3G8eHnIYQX6Gbjc5vulISf"],5))