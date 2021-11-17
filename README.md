
# Setup

Work must be done in the virtual environment to keep dependencies consistent.

### Create environment:

```
python3 -m venv venv
```

### Activate environment (in project folder):

```
source venv/bin/activate
```

or:

```
venv\Scripts\activate.bat
```

### Install/Update requirements (environment should be activated):

```
python3 -m pip install -r requirements.txt
```

### Deactivate environment (in project folder):

```
deactivate
```

### Download Dataset

Download the [Spotify Million Playlist Dataset](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge).

Unzip it, keeping the name as `spotify_million_playlist_dataset` and move it to `src`.

### Get your Client ID and Client Secret

- Navigate to https://developer.spotify.com/dashboard/
- Log in or create a Spotify account
- Click `CREATE AN APP` and create the app
- Click on the app and you will see the client ID and client secret

### Set up Client ID and Client Secret in the project

Create a file named `.env` in the `src` directory with the following lines:
```
SPOTIFY_CLIENT_ID=<Your Client ID>
SPOTIFY_CLIENT_SECRET=<Your Client Secret>
```

### Create Track Attributes Dataset

After downloading the Spotify Million Playlist Dataset, the track attributes dataset needs to be created.

From the `src` directory, run
```
python objects/spotify_song_attribute_encoder.py
```

This will generate a folder `spotify_track_attributes` that holds the song attributes for a track_uri.
