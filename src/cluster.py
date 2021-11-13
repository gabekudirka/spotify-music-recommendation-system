from sklearn.cluster import MeanShift
from sklearn.cluster import KMeans

import numpy as np

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
        print(kmeans.__dict__)
        print(kmeans.predict([self.track_attributes_to_array(self.predict_track)]))
