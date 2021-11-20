from django.db import models

# Create your models here.
# Honestly not sure if this is the correct use for this file
class SongRec:
  # add any other feilds we find usefule  here
  def __init__(self, title, artist, url):
    self.title = title
    self.artist = artist
    self.url  = url

