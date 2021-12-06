import sys, os
from urllib import parse
sys.path.append('../../src')
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import loader

from .forms import NameForm
from .models import SongRec
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from settings import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID
from predict import PredictSongs



def index(request):
  recommended_songs = []
  print(request)
  if request.method == 'POST':
    form = NameForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      playlist_uri = data['playlist_uri']
      playlist_dictionary = get_playlist_tracks(playlist_uri)
      p = PredictSongs()
      predicted_songs = p.predict(playlist_dictionary, 10)
      formatted_songs = get_songs_details(predicted_songs)
      recommended_songs = formatted_songs[:500]
    #TODO send the recomemdations back
    # or not this is pretty solid already
    # for i in range(500):
    #   recommended_songs.append(SongRec("Dark Horse", "Katy Parry", "https://open.spotify.com/track/4jbmgIyjGoXjY01XxatOx6"))

  template  = loader.get_template('client/index.html')
  context = {
    'recommended_songs': recommended_songs
  }
  return HttpResponse(template.render(context, request))


def get_songs_details(songs):
  tracks = []

  # setup connection
  client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
  sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
  
  for song in songs:
    print(song)
    id = song['id'].split(':')[2]
    response = sp.track(id)
    tracks.append(SongRec(response['name'],response['artists']['name'],response['external_urls']['spotify']))
  
  return tracks

def get_playlist_tracks(playlist_url):
    # setup connection
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    #get playlist id 
    path = parse.urlparse(playlist_url).path
    path, playlist_id = path.split('playlist/',1)
    # get playlist
    playlist = sp.playlist_items(playlist_id=playlist_id)
    
    #parse into dictionary
    tracks = {}
    for item in playlist['items']:
      # get features
      features = sp.audio_features([item['track']['id']])
      attributes = {}
      attributes['danceability'] = features[0]['danceability']
      attributes['energy']= features[0]['energy']
      attributes['key']= features[0]['key']
      attributes['loudness']= features[0]['loudness']
      attributes['mode']= features[0]['mode']
      attributes['speechiness']= features[0]['speechiness']
      attributes['acousticness']= features[0]['acousticness']
      attributes['instrumentalness']= features[0]['instrumentalness']
      attributes['liveness']= features[0]['liveness']
      attributes['valence']= features[0]['valence']
      attributes['tempo']= features[0]['tempo']
      attributes['type']= 'audio_features'
      attributes['id']= item['track']['id']
      attributes['uri']= item['track']['uri']
      attributes['track_href']= item['track']['href']
      attributes['analysis_url']= features[0]['analysis_url']
      attributes['duration_ms']= item['track']['duration_ms']
      attributes['time_signature']= features[0]['time_signature']
      # add to tracks dictionary
      tracks[f"spotify:track:{item['track']['id']}"] = attributes

    return tracks
    
    

    
    
