from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import loader

from .forms import NameForm
from .models import SongRec

def index(request):
  recommended_songs = []
  print(request)
  if request.method == 'POST':
    form = NameForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      playlist_uri = data['playlist_uri']

    #TODO recommend songs here
    # or not this is pretty solid already
    for i in range(500):
      recommended_songs.append(SongRec("Dark Horse", "Katy Parry", "https://open.spotify.com/track/4jbmgIyjGoXjY01XxatOx6"))

  template  = loader.get_template('client/index.html')
  context = {
    'recommended_songs': recommended_songs
  }
  return HttpResponse(template.render(context, request))

