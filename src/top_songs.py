from objects.spotify_song_attribute_decoder import TrackAttributeDecoder
from sklearn import preprocessing
from scipy import spatial

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

    def mse(self, song, target):
        if song is None:
            return 1000000000
        totalDif = 0
        for attribute in self.attributes:
            totalDif += (target[attribute] - song[attribute ])**2
        return totalDif

    def cosine_similarity(self, song, target):
        if song is None:
            return 0
        return 1 - spatial.distance.cosine(song, target)

    # def get_similar_songs(self, songs, target, n):
    #     numSongs = len(songs)
    #     print('Number of songs:', numSongs)
    #     songs[self.attributes] = preprocessing.Normalizer().fit_transform(songs[self.attributes])
    #     target[self.attributes] = preprocessing.Normalizer().transform(target[self.attributes])

    #     #songs_dict = songs.set_index('track_id').T.to_dict('dict')
    #     topSongs = {}

    #     for key, val in songs[self.attributes].iterrows():
    #         target_vals = target[self.attributes].values[0]
    #         score = self.cosine_similarity(val.values,target_vals)
    #         topSongs[key]=score
    #     sortedSongs = {k: v for k, v in sorted(topSongs.items(), key=lambda item: item[1], reverse=True)}
    #     return list(sortedSongs.items())[:n]

    def get_similar_songs(self, songs, target, n):
            numSongs = len(songs)
            print('Number of songs:', numSongs)

            songs[self.attributes] = preprocessing.Normalizer().fit_transform(songs[self.attributes])
            target[self.attributes] = preprocessing.Normalizer().transform(target[self.attributes])

            #songs_dict = songs.set_index('track_id').T.to_dict('dict')
            topSongs = {}
            idx = 0

            for key, val in songs[self.attributes].iterrows():
                target_vals = target[self.attributes].values[0]
                score = self.cosine_similarity(val.values,target_vals)
                #only keeps smallest n items so no sorting is necessary at the end
                if idx >= n:
                    smallest_so_far = min(topSongs.values())
                    if score > smallest_so_far:
                        topSongs = {k:v for k,v in topSongs.items() if v != smallest_so_far}
                        #topSongs.pop(min(topSongs, key=topSongs.get))
                        topSongs[key] = score
                else:
                    topSongs[key] = score
                idx += 1

            return topSongs

if __name__ == '__main__':
    d = TrackAttributeDecoder()
    d.decode_attribute_files(1000)
    #print(d.tracks.keys())

    t = TopSongs()
    print(t.get_similar_songs(d.tracks, d.tracks["spotify:track:4Ju7C4g69ObdLrVO5qh1ks"], 5))
