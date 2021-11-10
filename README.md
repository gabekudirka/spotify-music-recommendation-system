
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

Download the dataset from https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge. Unzip it, keeping the name as `spotify_million_playlist_dataset` and drag it into your working directory.
