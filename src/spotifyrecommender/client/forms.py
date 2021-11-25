from django import forms

class NameForm(forms.Form):
  your_name = forms.CharField(label='playlist_uri', max_length=100)