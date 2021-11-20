from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import SongRec

def index(request):
  recommended_songs = []
  for i in range(20):
    recommended_songs.append(SongRec("Dark Horse", "Katy Parry", "https://open.spotify.com/track/4jbmgIyjGoXjY01XxatOx6"))
  template  = loader.get_template('client/index.html')
  context = {
    'recommended_songs': recommended_songs
  }
  return HttpResponse(template.render(context, request))

