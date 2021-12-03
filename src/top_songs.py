from objects.spotify_song_attribute_decoder import TrackAttributeDecoder
from sklearn import preprocessing
from sklearn.metrics.pairwise import cosine_similarity

class TopSongs:
    def __init__(self):
        self.attributes = [ "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
        
    def normalize_attr(self, songs):
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

    def normalize_attr_sklearn(self, songs):
        normalized_songs = preprocessing.Normalizer().fit_transform(songs[self.attributes])
        for key, vals in songs.items():
            for attribute in self.attributes:
                if vals is not None:
                    songs[key][attribute] = normalize([vals[attribute]])

    def mse(self, song, target):
        if song is None:
            return 1000000000
        totalDif = 0
        for attribute in self.attributes:    
            totalDif += (target[attribute] - song[attribute ])**2
        return totalDif

    def get_similar_songs(self, songs, target, n):
        numSongs = len(songs)
        print('Number of songs:', numSongs)
        #self.normalize_attr_sklearn(songs)
        songs[self.attributes] = preprocessing.Normalizer().fit_transform(songs[self.attributes])
        target = preprocessing.Normalizer().transform(target[self.attributes])
        songs_dict = songs.set_index('track_id').T.to_dict('dict')
        topSongs = {}

        for key, val in songs_dict.items():
            score = self.mse(val,target)
            topSongs[key]=score
        sortedSongs = {k: v for k, v in sorted(topSongs.items(), key=lambda item: item[1])}
        return list(sortedSongs.items())[:n]


        

if __name__ == '__main__':
    d = TrackAttributeDecoder()
    d.decode_attribute_files()
    #print(d.tracks.keys())
    t =TopSongs()
    print(t.get_similar_songs(d.tracks,d.tracks["spotify:track:3G8eHnIYQX6Gbjc5vulISf"],5))