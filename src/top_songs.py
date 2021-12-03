from objects.spotify_song_attribute_decoder import TrackAttributeDecoder
from sklearn.preprocessing import normalize 

class TopSongs:
    def __init__(self):
        self.attributes = [ "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
        
    def normalizeAttr(self, songs):
        print('normalizing song attributes')
        mins = dict.fromkeys(self.attributes,10000000000)
        maxs = dict.fromkeys(self.attributes,-10000000000)
        index = 0
        for key, vals in songs.items():
            #print(f'- getting min/max { index + 1 }/{ numSongs}: { key }          ', end='\r')
            index += 1
            for attribute in self.attributes:                
                if vals is not None:
                    mins[attribute] = min(vals[attribute], mins[attribute])
                    maxs[attribute] = max(vals[attribute], maxs[attribute])
        normSongs = songs
        index = 0
        for key, vals in songs.items():
            #print(f'- normalizing { index + 1 }/{ numSongs}: { key }          ', end='\r')
            index += 1
            for attribute in self.attributes:
                if vals is not None:
                    if maxs[attribute]-mins[attribute] != 0:
                        normSongs[key][attribute] = (vals[attribute] - mins[attribute])/(maxs[attribute]-mins[attribute])
                    else:
                         normSongs[key][attribute] = vals[attribute]
        return normSongs

    def mse(self, song, target):
        if song is None:
            return 1000000000
        totalDif = 0
        for attribute in self.attributes:    
            totalDif += (target[attribute] - song[attribute ])**2
        return totalDif

    def getSimilarSongs(self, songs, target, n):
        numSongs = len(songs)
        print('Number of songs:', numSongs)
        self.normalizeAttr(songs)
        topSongs = {}
        index = 0
        print('getting similar songs')
        for key, val in songs.items():
            #print(f'- getting similarity { index + 1 }/{ numSongs}: { key }          ', end='\r')
            index += 1
            score = self.mse(val,target)
            topSongs[key]=score
        sortedSongs = {k: v for k, v in sorted(topSongs.items(), key=lambda item: item[1])}
        return list(sortedSongs.items())[:n]


        

if __name__ == '__main__':
    d = TrackAttributeDecoder()
    d.decode_attribute_files()
    #print(d.tracks.keys())
    t =TopSongs()
    print(t.getSimilarSongs(d.tracks,d.tracks["spotify:track:3G8eHnIYQX6Gbjc5vulISf"],5))