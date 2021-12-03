import pickle
import pandas as pd
from sklearn.mixture import GaussianMixture
from collections import Counter, OrderedDict
from top_songs import TopSongs
from objects.spotify_song_attribute_decoder import TrackAttributeDecoder
import random


class PredictSongs():

    def __init__(self):
        with open('src/audio_features_gmm.pickle', 'rb') as f:
            self.audio_model = pickle.load(f)
        self.all_songs = pd.read_csv('src/audio_features_with_labels.csv')
        self.all_songs.rename(columns={'Unnamed: 0': 'track_id'}, inplace=True)
        self.audio_features = ['time_signature', 'key', 'mode', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'tempo']
        self.top_songs = TopSongs()
        

    #This assumes the playlist is just a list of tracks ids
    def predict(self, playlist, num_songs, model_name = 'audio'):
        if model_name == 'audio':
            model = self.audio_model
        
        all_related_songs = []
        for uri, features in playlist.items():
            track_data = self.all_songs.loc[self.all_songs['id'] == features['id']]
            track_features = track_data[self.audio_features]
            #can change this to take top n clusters - right now it just gets highest likelihood cluster
            predicted_cluster_label = model.predict(track_features)[0]
            #get all songs in that cluster
            cluster = self.all_songs.loc[self.all_songs['labels'] == predicted_cluster_label]
            related_songs = cluster.set_index('track_id').T.to_dict('dict')
            #Get the most similar songs in that cluster
            best_related_songs = self.top_songs.get_similar_songs(cluster, features, 50)
            all_related_songs.append(best_related_songs)
        
        #sort the list based on the frequency of the songs
        all_related_songs = [track[0] for sublist in all_related_songs for track in sublist]
        related_songs_sorted = [item for items, c in Counter(all_related_songs).most_common() for item in [items] * c]
        related_songs_sorted = list(OrderedDict.fromkeys(related_songs_sorted))
        #return top n most frequently occuring songs
        return related_songs_sorted[:num_songs]


if __name__ == '__main__':
    p = PredictSongs()
    t = TrackAttributeDecoder()
    t.decode_attribute_files(1)

    result = p.predict(dict(random.sample(t.tracks.items(), 10)), 10)
    print(result)