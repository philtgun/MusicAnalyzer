from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.utils import timezone

import sys
from urllib.request import urlretrieve, urlopen
import librosa
import soundfile as sf 
import io
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .models import Track

# spotify credentials 
client_credentials_manager = SpotifyClientCredentials(client_id='34ac9f95d773412c8a2fabd9bef03ebc',
                                                      client_secret='7c0022360e334a89b7a0f098cc0a99cc')
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def search_form(request):
    mytracks = Track.objects.order_by('created_date')
    return render(request, 'retrieval/search_form.html', {'mytracks': mytracks})


def search(request):
    if 'q' in request.GET and request.GET['q']: 
        q = request.GET['q']

        result = spotify.search(q, type='track', limit=30)
        tracks = result['tracks']
        print (len(result))

        tracks = spotify.search(q, type='track')['tracks']['items']

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

    ''' load album image '''
    track_url = "http://open.spotify.com/track/" + current_track.track_id 
    track_page = urlopen(track_url)
    soup = BeautifulSoup(track_page, 'html.parser')
    track_img = soup.find('img', class_="cover")
    
    ''' download audio '''
    print ("url", current_track.preview_url) 
    if current_track.preview_url:
        audio_filename = current_track.preview_url.split("/")[-1].split("?")[0]
        # print (current_track.preview_url)
        # url = "http://tinyurl.com/shepard-risset"
        # data, samplerate = sf.read(io.BytesIO(urlopen(url).read()))
        # data, sr = sf.read(io.BytesIO(urlopen(current_track.preview_url).read()))

        # urlretrieve(current_track.preview_url, audio_filename + ".wav")
        # y, sr = librosa.load(audio_filename + '.wav', sr=22050)
    else :
        audio_filename = None


    return render(request, 'retrieval/track_info.html', {'current_track':current_track, 'features': features, 'img_src': track_img['src']})


def analyize_features(request):
    all_tracks = Track.objects.all()
    all_track_ids = []
    for track in all_tracks:
        all_track_ids.append(track.uri)
    
    all_features = spotify.audio_features(all_track_ids)

    return render(request, 'retrieval/analyze_features.html', {'all_features': all_features})
