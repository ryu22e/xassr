from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def home(request):
    c = RequestContext(request)
    return render_to_response('home.html', c)