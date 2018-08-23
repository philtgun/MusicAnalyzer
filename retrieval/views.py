from django.shortcuts import render
from django.http import HttpResponse

import spotipy
import sys
import pprint
from spotipy.oauth2 import SpotifyClientCredentials

from .models import Track

client_credentials_manager = SpotifyClientCredentials(client_id='34ac9f95d773412c8a2fabd9bef03ebc',
                                                      client_secret='7c0022360e334a89b7a0f098cc0a99cc')
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create your views here.
def search_form(request):
    tracks = Track.objects.order_by('created_date')
    return render(request, 'retrieval/search_form.html', {'tracks': tracks})


def search(request):
    if 'q' in request.GET and request.GET['q']: 
        q = request.GET['q']

        result = spotify.search(q, type='track')
        tracks = result['tracks']
        print (len(result))

        tracks = spotify.search(q, type='track')['tracks']['items']

        # pprint.pprint(result['tracks']['items'])
        '''
        for i in range(len(tracks)) : 
            pprint.pprint (result[i]['uri'])
            pprint.pprint (result[i]['preview_url'])
            pprint.pprint (result[i]['name'])
            pprint.pprint (result[i]['duration_ms'])
            pprint.pprint (result[i]['album']['name'])
        '''


        return render(request, 'retrieval/search_results.html', {'tracks':tracks, 'query':q})
        
    else :
        message = 'You submitted empty form'
    
        return HttpResponse(message)


def add_track(request, id):
    print (id)
    return HttpResponse("hello")