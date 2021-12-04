from django import forms

class NameForm(forms.Form):
  playlist_uri = forms.CharField(label='playlist_uri', max_length=100)