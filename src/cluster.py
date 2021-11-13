from sklearn.cluster import MeanShift
from sklearn.cluster import KMeans

import numpy as np
import pprint

class TrackClusterer:
    def __init__(self, tracks, predict_track):
        self.tracks = tracks
        self.predict_track = predict_track

    def track_attributes_to_array(self, track):
        a = []
        a.append(hash(track.artist_name))
        a.append(hash(track.track_name))
        a.append(hash(track.album_name))
        return a

    def cluster(self):
        b = list(map(self.track_attributes_to_array, self.tracks))
        X = np.array(b)
        # clustering = MeanShift(bandwidth=2).fit(X)
        # print(clustering.__dict__)
        # print(clustering.predict([self.track_attributes_to_array(self.predict_track)]))

        kmeans = KMeans(n_clusters = 5, random_state = 0).fit(X)
        cluster_prediction = kmeans.predict([self.track_attributes_to_array(self.predict_track)])
        # print(kmeans.predict([self.track_attributes_to_array(self.predict_track)]))

        # get songs from cluster prediction
        cluster_labels = kmeans.labels_

        recommended_songs = []

        for i in range(0, len(list(cluster_labels))):
            if cluster_labels[i] == cluster_prediction:
                recommended_songs.append(self.tracks[i])


        print(f'Given song: { self.predict_track.track_name }')
        print(f'Recommended Songs:')
        pprint.pprint(list(map(lambda t: t.track_name, recommended_songs)))
