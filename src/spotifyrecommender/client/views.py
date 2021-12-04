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


def index(request):
  recommended_songs = []
  print(request)
  if request.method == 'POST':
    form = NameForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      playlist_uri = data['playlist_uri']
      print("\n\n\n\n look here", playlist_uri)
    # get_playlist_tracks('https://open.spotify.com/playlist/37i9dQZF1EUMDoJuT8yJsl?si=4f31c7c179524b6a')
    #TODO recommend songs here
    
    # or not this is pretty solid already
    for i in range(500):
      recommended_songs.append(SongRec("Dark Horse", "Katy Parry", "https://open.spotify.com/track/4jbmgIyjGoXjY01XxatOx6"))

  template  = loader.get_template('client/index.html')
  context = {
    'recommended_songs': recommended_songs
  }
  return HttpResponse(template.render(context, request))

def get_playlist_tracks(playlist_url):
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    path= parse.urlparse(playlist_url).path
    path, playlist_url = path.split('playlist/',1)
    print("playlist id is: ", playlist_url)
    # playlist_items = sp.playlist_items()
    
