import spotipy
import sys
import pprint
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='34ac9f95d773412c8a2fabd9bef03ebc',
                                                      client_secret='7c0022360e334a89b7a0f098cc0a99cc')
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

search_str = 'shofukan'

result = spotify.search(search_str, type='track')['tracks']['items']

# pprint.pprint(result['tracks']['items'])
for i in range(len(result)) : 
    pprint.pprint (result[i]['uri'])
    pprint.pprint (result[i]['preview_url'])
    pprint.pprint (result[i]['name'])
    pprint.pprint (result[i]['duration_ms'])
    pprint.pprint (result[i]['album']['name'])