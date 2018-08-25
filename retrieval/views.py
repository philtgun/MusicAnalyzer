from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.utils import timezone

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
    mytracks = Track.objects.order_by('created_date')
    return render(request, 'retrieval/search_form.html', {'mytracks': mytracks})


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

        mytracks = Track.objects.order_by('created_date')

        return render(request, 'retrieval/search_results.html', {'mytracks':mytracks, 'tracks':tracks, 'query':q})
        
    else :
        message = 'You submitted empty form'
    
        return HttpResponse(message)


def add_track(request, id):
    # analysis = spotify.audio_features('spotify:track:' + id)
    # print (analysis)
    selected_track = spotify.track('spotify:track:' + id)
    track = Track()
    track.track_name = selected_track['name']
    track.artist = selected_track['artists'][0]['name']
    track.uri = 'spotify:track:' + id
    track.track_id = id
    track.preview_url = selected_track['preview_url']
    track.created_date = timezone.now()
    track.save()

    return redirect('search_form')


def delete_track(request, id):
    deleting_track = Track.objects.get(pk=id).delete()
    return redirect('search_form')

def track_info(request, id):
    current_track = Track.objects.get(pk=id)
    features = spotify.audio_features([current_track.uri])
    print (features)
    return render(request, 'retrieval/track_info.html', {'current_track':current_track, 'features': features})


def analyize_features(request):
    all_tracks = Track.objects.all()
    print (all_tracks)
    all_track_ids = []
    for track in all_tracks:
        all_track_ids.append(track.uri)
    
    all_features = spotify.audio_features(all_track_ids)

    return render(request, 'retrieval/analyze_features.html', {'all_features': all_features})
