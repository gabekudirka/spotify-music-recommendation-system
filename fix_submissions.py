import json
import numpy as np
import pandas as pd
import random
import sys

from src.objects.spotify_song_attribute_decoder import TrackAttributeDecoder

if __name__ == '__main__':
    t = TrackAttributeDecoder()
    t.decode_attribute_files()

    f = open('challenge_set.json')
    data = json.load(f)

    f.close()

    challenge_playlists = data['playlists']

    pidded = {}

    for playlist in challenge_playlists:
        track_uris = [track["track_uri"] for track in playlist["tracks"]]
        pidded[playlist["pid"]] = set(track_uris)

    corrected_submission = open('corrected_submission.csv', "w")

    f = open('asubmission.csv')
    for line_no, line in enumerate(f):
        line = line.strip()
        if not line:
            continue

        if line.startswith("team_info"):
            corrected_submission.write(line)
            corrected_submission.write('\n')
            continue

        fields = line.split(",")
        fields = [f.strip() for f in fields]

        pid = int(fields[0])

        tracks = fields[1:]

        referenced_challenge_playlist = list(filter(lambda x: x['pid'] == pid, challenge_playlists))[0]

        intersecting_tracks = pidded[pid].intersection(set(tracks))

        if intersecting_tracks:
            print(f'Seed tracks in submission for { pid }')

            for intersecting_track in intersecting_tracks:
                tracks.remove(intersecting_track)

                new_track = random.sample(list(t.tracks.keys()), 1)[0]

                while new_track in intersecting_tracks:
                    new_track = random.sample(t.tracks.keys(), 1)

                tracks.append(new_track)

        fixed = [f'{ pid }'] + tracks

        corrected_submission.write(','.join(fixed))
        corrected_submission.write('\n')
