from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import loader

def index(request):
  template  = loader.get_template('client/index.html')
  context = {}
  return HttpResponse(template.render(context, request))
