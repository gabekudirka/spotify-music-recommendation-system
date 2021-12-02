from objects.spotify_song_attribute_decoder import TrackAttributeDecoder
import numpy

class TopSongs:

    def mse(song, target):
        totalDif = 0
        attributes = [ "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
        for attribute in attributes:
            totalDif += (target[attribute] - song[attribute ])**2
        return totalDif

    def getSimilarSongs(self, songs, target, n):
        topSongs = {}
        for key, val in songs:
            score = mse(val,target[0])
            topSongs[key]=score
        sortedSongs = sorted(topSongs, key=topSongs.get, reverse=True)
        for song in sortedSongs:
            print(topSongs,song)

        return sortedSongs


        

if __name__ == '__main__':
    d = TrackAttributeDecoder()
    d.decode_attribute_files()
    print(d.tracks.keys())
    getSimilarSongs(d.tracks,d.tracks['6exe9pbk1gLudSijdPau0K'],10)