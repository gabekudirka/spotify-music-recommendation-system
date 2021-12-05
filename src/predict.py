import pickle
import pandas as pd
from sklearn.mixture import GaussianMixture
from collections import Counter, OrderedDict
from top_songs import TopSongs
from objects.spotify_song_attribute_decoder import TrackAttributeDecoder
import random


class PredictSongs():

    def __init__(self, sample_tracks):
        pd.options.mode.chained_assignment = None  # default='warn'
        print("Loading pickle model")
        with open('src/audio_features_gmm.pickle', 'rb') as f:
            self.audio_model = pickle.load(f)

        self.audio_features = ['time_signature', 'key', 'mode', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'tempo']
        self.top_songs = TopSongs()

        self.all_songs = pd.read_csv('src/audio_features_with_labels.csv')
        self.all_songs.rename(columns={'Unnamed: 0': 'track_id'}, inplace=True)
        self.all_songs.set_index('track_id', inplace=True)

        self.clusters = {i: self.all_songs.loc[self.all_songs['labels'] == i] for i in range(self.audio_model.n_components)}
        self.sample_tracks = sample_tracks
        self.prediction_count = 0


    #This assumes the playlist is just a list of tracks ids
    def predict(self, playlist, num_songs, model_name = 'audio'):

        self.prediction_count += 1

        print(f"Predicting { self.prediction_count }")

        # just get random songs if given none
        if len(playlist) == 0:
            return self.get_random_recommendations(num_songs)

        if model_name == 'audio':
            model = self.audio_model

        all_related_songs = []

        for uri, features in playlist.items():

            print(f'Getting similar tracks for track: { uri }')

            track_data = pd.DataFrame.from_dict(dict(uri=features), orient='index')
            track_features = track_data[self.audio_features]
            #can change this to take top n clusters - right now it just gets highest likelihood cluster
            predicted_cluster_label = model.predict(track_features)[0]
            #get all songs in that cluster
            cluster = self.clusters[predicted_cluster_label]
            #related_songs = cluster.set_index('track_id').T.to_dict('dict')
            #Get the most similar songs in that cluster
            best_related_songs = self.top_songs.get_similar_songs(cluster, track_features, 100)
            all_related_songs.append(best_related_songs)

        #sort the list based on the frequency of the songs
        all_related_songs = [track for sublist in all_related_songs for track in sublist.keys()]
        related_songs_sorted = [item for items, c in Counter(all_related_songs).most_common() for item in [items] * c]

        #remove duplicates
        related_songs_sorted = list(OrderedDict.fromkeys(related_songs_sorted))

        #return top n most frequently occuring songs

        for seed_track in playlist:
            related_songs_sorted = list(filter(lambda a: a != seed_track, related_songs_sorted))

        print(f'Got { len(related_songs_sorted) } related tracks after filtering out seed tracks')

        if len(related_songs_sorted) < 500:
            diff = 500 - len(related_songs_sorted)
            print(f"Not 500 tracks with { diff } tracks needed, pad with random tracks at end")

            random_tracks = random.sample(list(self.sample_tracks.keys()), diff)

            related_songs_sorted += random_tracks

        return related_songs_sorted[:num_songs]

    def get_random_recommendations(self, num_songs):
        return list(dict(random.sample(self.sample_tracks.items(), num_songs)))


if __name__ == '__main__':
    t = TrackAttributeDecoder()
    t.decode_attribute_files(1)

    p = PredictSongs(t.tracks)

    tracks = dict(random.sample(t.tracks.items(), 10))

    result = p.predict(tracks, 10)
    print(result)
